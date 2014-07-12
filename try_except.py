import os;
os.chdir('E:\\Project\gitLearning\python')
data =open('sketch.txt')
for item in data:
    try:
        (man,word)= item.split(':',1)
        print(man,end=' ')
        print('said:',end=' ')
        print(word,end='')
    except:
        pass
data.close()
