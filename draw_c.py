import csv
import time
import traceback
import ctypes
import os
import struct
from ctypes import *

from pymouse import PyMouse
from pykeyboard import PyKeyboard



class Action(object):

	def __init__(self, file):
		self.file = file
		self.m = PyMouse()
		self.k = PyKeyboard()

	def action_read(self):
	# 从filename中读取操作序列
		action_list = []
		with open(self.file) as f:
			f_csv = csv.reader(f)
			for row in f_csv:
				action_list.append(row)
		return action_list

	def key_translate(self, key_data):
	# 识别序列中的键
		if len(key_data) == 1:
			return key_data
		elif len(key_data) == 2 and key_data.startswith('F'):
			return self.k.function_keys[int(key_data[1])]
		elif key_data == 'enter':
			return self.k.enter_key
		elif key_data == 'space':
			return self.k.space_key
		elif key_data == 'control':
			return self.k.control_key
		elif key_data == 'alt':
			return self.k.alt_key
		else:
			raise Exception("未定义此操作！")

	def action_translte(self, action_unit):
	# 将序列语言翻译成指令
		if action_unit[0] == '0':
			try:
				xy = eval(action_unit[1])
			except Exception as e:
				return False
			x,y = xy[0], xy[1]
			self.m.click(x, y, 1)
			return True
		elif action_unit[0] == '1':
			try:
				keyboard_action_list = action_unit[1].split('_')
				if keyboard_action_list[0] == 'tap':  # 敲击某个键
					self.k.tap_key(key_data)
				elif keyboard_action_list[0] == 'press': # 按住某个键
					key_data = self.key_translate(keyboard_action_list[1])
					self.k.press_key(key_data)
				elif keyboard_action_list[0] == 'presses': # 按住某两个键
					key_data1 = self.key_translate(keyboard_action_list[1])
					key_data2 = self.key_translate(keyboard_action_list[2])
					self.k.press_keys([key_data1, key_data2])
				elif keyboard_action_list[0] == 'release': # 松开某个键
					key_data = self.key_translate(keyboard_action_list[1])
					self.k.release_key(key_data)
				elif keyboard_action_list[0] == 'type': # 输入
					self.k.type_string(keyboard_action_list[1])
				elif keyboard_action_list[0] == 'callcpp':

					x = int(keyboard_action_list[1])
					y = int(keyboard_action_list[2])

					#i_path = keyboard_action_list[3]
					#t_path = keyboard_action_list[4]

					result, x_t, y_t = call_c(x, y)
					#x_tt = x_t.value
					#y_tt = y_t.value
					print(x_t, y_t)
					x_tt = x_t.value
					y_tt = y_t.value
					self.k.type_string(str(x_tt) + '_' + str(y_tt))
				elif keyboard_action_list[0] == 'drawc':

					self.draw_circle()


			except Exception:
				traceback.print_exc()
				return False
		else:
			print("对象输入错误")
			return False

	def run(self):
		action_list = self.action_read()
		action_lens = len(action_list)
		for i in range(1, action_lens):
			self.action_translte(action_list[i])
			delay = eval(action_list[i][2])######################################################???????????????????????????????
			time.sleep(delay)

	def draw_circle(self):

		self.m.click(421, 62, 1)
		self.m.click(422, 61, 1)
		self.m.click(419, 59, 1)
		time.sleep(0.5)
		self.m.press(421, 500)
		time.sleep(0.5)
		self.m.move(600,500)
		time.sleep(0.5)
		self.m.move(600, 670)
		time.sleep(0.5)
		self.m.release(600, 600)

        # type some words
		self.m.click(293, 68)
		self.m.click(478, 549)
		self.k.type_string("Hello World!")


def task_example():
	# 新建txt文档，输入Hello, World!，然后保存为123.txt
	k.press_key(k.control_key) #按住Ctrl
	k.tap_key('n')  #新建
	k.release_key(k.control_key) #松开Ctrl
	k.type_string('Hello, World!')  #输入 ‘Hello, World!’

	k.press_key(k.control_key) #按住Ctrl
	k.tap_key('s')
	k.release_key(k.control_key) #松开Ctrl
	k.type_string('123')
	k.tap_key(k.enter_key)



if __name__ == '__main__':
	a = Action('action1.csv')
	a.run()
