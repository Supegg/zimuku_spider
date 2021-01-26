'''
分析字幕文件中出现的所有英文单词，并累计出现的次数
统计单词中所有字母的频次

steps:
    1. 识别文件类型，txt、rar、zip
        zip: 50 4B 03
        rar: 52 61 72 21 1A 07 00
        else:
    2. 打开/解压文件
        7z x 14.zip -y -oE:\tmp
    3. 提取单词
    4. 统计

https://blog.csdn.net/weixin_42902669/article/details/102806154
'''
import os
import shutil
import re
import subprocess
import json
import stat


class data():
    def __init__(self):
        self.words = dict()
        self.letters = dict()

        for i in range(65, 91):
            self.letters[chr(i)] = 0
        for i in range(97, 123):
            self.letters[chr(i)] = 0

    def add_word(self, word):
        # print('add_word: ', word)
        if word in self.words:
            self.words[word] += 1
        else:
            self.words[word] = 1

        for a in word:
            self.letters[a] += 1

    def save(self, filename):
        with open(f'{results}\{filename}_letters.json', mode='wt') as f:
            f.write(json.dumps(sorted(self.letters.items(),
                                      key=lambda i: i[1], reverse=True)))

        with open(f'{results}\{filename}_words.json', mode='wt') as f:
            f.write(json.dumps(sorted(self.words.items(),
                                      key=lambda i: i[1], reverse=True)))

    def save_total(dl: list):
        words = dict()
        letters = dict()

        for i in range(65, 91):
            letters[chr(i)] = 0
        for i in range(97, 123):
            letters[chr(i)] = 0

        for d in dl:
            for k, v in d.letters.items():
                letters[k] += v

            for k, v in d.words.items():
                if k in words:
                    words[k] += v
                else:
                    words[k] = v

        with open(f'{results}\\total_letters.json', mode='wt') as f:
            f.write(json.dumps(sorted(letters.items(),
                                      key=lambda i: i[1], reverse=True)))

        with open(f'{results}\\total_words.json', mode='wt') as f:
            f.write(json.dumps(sorted(words.items(),
                                      key=lambda i: i[1], reverse=True)))


ds = 'requests\\download'
# ds = 'test'
tmp = os.path.join(os.getcwd(), '.tmp')
results = 'results'


def get_file_type(file):
    '''
    判断文件类型：txt, zip,  rar
    '''
    if os.path.getsize(file) < 8:
        return 'txt'

    with open(file, 'rb') as f:
        bs = f.read(8)
        if bs[0] == 0x50 and bs[1] == 0x4B and bs[2] == 0x03:
            return 'zip'
        elif bs[0] == 0x52 and bs[1] == 0x61 and bs[2] == 0x72:
            return 'rar'
        else:
            return 'txt'


def readonly_handler(func, path, execinfo):
    '''
    PermissionError: [WinError 5] 拒绝访问
    '''
    os.chmod(path, stat.S_IWRITE)
    func(path)


def mk_tmp():
    if os.path.exists(tmp):
        shutil.rmtree(tmp, onerror=readonly_handler)
        os.mkdir(tmp)
    else:
        os.mkdir(tmp)


def unfile(file):
    mk_tmp()
    # os.popen(f"7z x {file} -y -o{tmp}")
    ex=subprocess.Popen(f"7z x {file} -y -o{tmp}",
                          stdout = subprocess.PIPE, shell = True)
    out, err=ex.communicate()
    status=ex.wait()
    # print("cmd out: ", out.decode('gbk'))


def yield_tmp():
    for path, dir_list, file_list in os.walk('.tmp'):
        for file in file_list:
            f=os.path.join(path, file)
            yield f


def get_files(file):
    t=get_file_type(file)

    if t == 'txt':
        yield file
        return

    if t == 'rar' or t == 'zip':
        unfile(file)

    for f in yield_tmp():
        yield f


def da(file):
    d=data()
    r=re.compile(r'\b([A-Za-z]+)\b')
    rl = re.compile(r"}([a-zA-Z\d\s,\.?!']+)\n") # 取对白部分

    with open(file, mode = 'rt', encoding = 'utf-8', errors = 'ignore') as f:
        fl = f.readline().replace('\x00', '')
        if '[Script Info]' in fl:
            suf = 'ass'
        else:
            suf = 'srt'

        for line in f:
            line=line.replace('\x00', '')

            if suf=='ass':
                line = line.replace('{\\r}', '')
                m = rl.search(line)
                if m:
                    line = m.group(1)
                else:
                    continue

            # print(line)
            for m in r.finditer(line):
                w=m.group(1)
                d.add_word(w)

    return d


if __name__ == '__main__':
    if(os.path.exists(results)):
        shutil.rmtree(results)
    os.mkdir(results)

    dl=list()
    for path, dir_list, file_list in os.walk(ds):
        for file in file_list:
            f=os.path.join(path, file)
            for fp in get_files(f):
                print(fp)
                d=da(fp)
                d.save(os.path.basename(fp))
                dl.append(d)
    data.save_total(dl)
