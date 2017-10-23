# -*- coding: utf-8 -*-

>>> lan_list = ['c', 'c++', 'c#', 'Java', 'Ruby', 'Python', 'Javascript']
>>> lan_list[0] = 'C是一门运行速度很快的语言。'
>>> print(lan_list)
['C是一门运行速度很快的语言。', 'c++', 'c#', 'Java', 'Ruby', 'Python', 'Javascript']
>>> lan_list[1:3] = ['C++在C的基础上增加了面向对象的特性', 'C#在游戏开发领域（Unity引擎）方面运用广泛']
>>> print(lan_list)
['C是一门运行速度很快的语言。', 'C++在C的基础上增加了面向对象的特性', 'C#在游戏开发领域（Unity引擎）方面运用广泛', 'Java', 'Ruby', 'Python', 'Javascript']
