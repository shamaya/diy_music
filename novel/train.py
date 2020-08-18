'''
@lanhuage: python
@Descripttion: 
@version: beta
@Author: xiaoshuyui
@Date: 2020-06-17 16:43:32
@LastEditors: xiaoshuyui
@LastEditTime: 2020-07-16 15:49:35
'''
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
import numpy as np
import os

# 加载数据文件
if os.path.exists('D:\\testALg\\Diy-musics\\novel\\static\\nz.npy'):
    text = np.load('D:\\testALg\\Diy-musics\\novel\\static\\nz.npy',allow_pickle=True)
    # text = text[0]
else:
    with open('D:\\testALg\\Diy-musics\\novel\\static\\nietzsche.txt', 'r') as f:
        text = f.read()
    np.save('D:\\testALg\\Diy-musics\\novel\\static\\nietzsche.npy',np.array(text))

print('corpus length:', len(text))

# 生成字符_id字典，有标点符号和a~z组成
chars = sorted(list(set(text)))
char_num = len(chars)
print('total chars:', char_num)
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40  # 每个句子由40个字符组成，也就是有40个cell
step = 3  # 每隔3个字符，获取maxlen个字符作为一个句子
sentences = []  # 存放句子的数组，每个句子是一个输入x
next_chars = []  # label，每个句子后边紧跟的字符作为输出y
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
# 训练数据转换为模型认识的格式，每个句子对应一个输出字符
# 训练数据x，维度(句子数，cell数，xi维度)
x = np.zeros((len(sentences), maxlen, char_num), dtype=np.bool)
# 训练label y，维度(句子数，yi维度)
y = np.zeros((len(sentences), char_num), dtype=np.bool)
# 将x,y转为one_hot，每个输入句子由maxlen个one_hot向量组成
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, char_num)))
model.add(Dense(char_num, activation='softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

def on_epoch_end(epoch, _):
    None


print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit(x, y,
          batch_size=128,
          epochs=10,
          callbacks=[print_callback])

# 存储模型
model.save('nz_model.h5')


