import wordcloud
import jieba

w = wordcloud.WordCloud()
w.generate('and that government of the people, by the people, for the people, shall not perish from the earth.')
w.to_file('output1.png')

# 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
w = wordcloud.WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc')
# 调用词云对象的generate方法，将文本传入
w.generate('从明天起，做一个幸福的人。喂马、劈柴，周游世界。从明天起，关心粮食和蔬菜。我有一所房子，面朝大海，春暖花开')
# 将生成的词云保存为output2-poem.png图片文件，保存到当前文件夹中
w.to_file('output2-poem.png')

# 从外部.txt文件中读取大段文本，存入变量txt中
f = open('关于实施乡村振兴战略的指导意见.txt', encoding='utf-8')
txt = f.read()
# 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc')
# 将txt变量传入w的generate()方法，给词云输入文字
w.generate(txt)
# 将词云图片导出到当前文件夹
w.to_file('output3-sentence.png')

# 中文分词第三方模块jieba
# 构建并配置词云对象w
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc')

# 调用jieba的lcut()方法对原始文本进行中文分词，得到string
txt = '同济大学（Tongji University），简称“同济”，是中华人民共和国教育部直属，由教育部、国家海洋局和上海市共建的全国重点大学，' \
      '历史悠久、声誉卓著，是国家“双一流”、“211工程”、“985工程”重点建设高校，也是收生标准最严格的中国大学之一'
txtlist = jieba.lcut(txt)
string = " ".join(txtlist)
# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)
# 将词云图片导出到当前文件夹
w.to_file('output4-tongji.png')

# 乡村振兴战略中央文件（五角星形状）
# 导入imageio库中的imread函数，并用这个函数读取本地图片，作为词云形状图片
import imageio
mk = imageio.imread("wujiaoxing.png")
w = wordcloud.WordCloud(mask=mk)
# 构建并配置词云对象w，注意要加scale参数，提高清晰度
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc',
                        mask=mk,
                        scale=15)
# 对来自外部文件的文本进行中文分词，得到string
f = open('关于实施乡村振兴战略的指导意见.txt', encoding='utf-8')
txt = f.read()
txtlist = jieba.lcut(txt)
string = " ".join(txtlist)
# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)
# 将词云图片导出到当前文件夹
w.to_file('output6-village.png')

# 新时代中国特色社会主义（中国地图形状）
mk = imageio.imread("chinamap.png")
w = wordcloud.WordCloud(mask=mk)
# 构建并配置词云对象w，注意要加scale参数，提高清晰度
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc',
                        mask=mk,
                        scale=15)
# 对来自外部文件的文本进行中文分词，得到string
f = open('新时代中国特色社会主义.txt', encoding='utf-8')
txt = f.read()
txtlist = jieba.lcut(txt)
string = " ".join(txtlist)
# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)
# 将词云图片导出到当前文件夹
w.to_file('output7-chinamap.png')

