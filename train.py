# coding: utf-8
import datetime
import time
# import clipboard  # Only Pythonista


class nexttrain:

    def __init__(self):
        self.__week_dict = {'[MON]': 0, '[TUE]': 1, '[WED]': 2,
                            '[THU]': 3, '[FRI]': 4, '[SAT]': 5, '[SUN]': 6, '[HOL]': 7}

    def __str__(self):
        return str(self.__file)

    def open(self, data):
        self.__rawfile = open(data, "r", encoding='utf-8')
        self.__read = self.__rawfile.readlines()
        self.__initfile()
        self.__delete_comment()
        self.__separate_block()
        self.__convert_dict()
        self.__make_dict()
        self.__make_list()

    def get_time(self, time, info=True):
        week = self.__dict_week_num[time.weekday()]
        writableh = time.hour
        shitatu = False
        if writableh > 0 and writableh < 5:
            hour = 5
            writableh = 5
            shitatu = True
        elif writableh == 0:
            hour = 19
        else:
            hour = writableh - 5

        for i in range(len(self.__file[week][hour])):
            num = int(self.__file[week][hour][i][2:])

            if i == 0:
                if time.minute < num or shitatu == True:
                    infotext = self.__return_info(
                        info, self.__file[week][hour][i])
                    if info:
                        return datetime.datetime(time.year, time.month, time.day, writableh, num), infotext
                    else:
                        return datetime.datetime(time.year, time.month, time.day, writableh, num)

            else:
                if i == (len(self.__file[week][hour])-1):
                    if time.minute >= num:
                        if hour != 19:
                            ret = int(self.__file[week][hour + 1][0][2:])
                            infotext = self.__return_info(
                                info, self.__file[week][hour + 1][0])
                            if writableh + 1 > 23:
                                day = time.day + 1
                                return datetime.datetime(time.year, time.month, day, (writableh + 1) % 24, ret), infotext
                            else:
                                return datetime.datetime(time.year, time.month, time.day, writableh+1, ret), infotext
                        else:
                            week = ((time.weekday() + 1) % 7)
                            week = self.__dict_week_num[week]
                            ret = int(
                                self.__file[week][0][0][2:])
                            infotext = self.__return_info(
                                info, self.__file[week][0][0])
                            day = time.day + 1
                            return datetime.datetime(time.year, time.month, day, 5, ret), infotext

                before = int(self.__file[week][hour][i-1][2:])

                if time.minute < num and time.minute >= before:
                    infotext = self.__return_info(
                        info, self.__file[week][hour][i])
                    return datetime.datetime(time.year, time.month, time.day, writableh, num), infotext

            # print(num)

    def __return_info(self, v, list):
        if v == True:
            text = self.__dic_destination[list[1]
                                          ] + self.__dic_destination[list[0]]
            return text
        else:
            return None

    def __initfile(self):
        self.__file = self.__read
        self.__rawfile.close()
        del self.__read
        del self.__rawfile

    def __delete_comment(self):
        self.__del = self.__file
        self.__file = []
        for i in range(len(self.__del)):
            if self.__del[i][0] != ';':
                self.__file.append(self.__del[i])
        del self.__del
        del self.__file[0]

    def __separate_block(self):
        self.__sep = self.__file
        self.__temp = []
        self.__file = [[]]
        i = 0
        flag = 0
        while i < len(self.__sep):
            if self.__sep[i][0] == '#':
                j = i - 1

                if flag == 0:
                    while flag < j-1:
                        self.__temp.append(self.__sep[flag])
                        flag += 1
                    self.__file.append(self.__temp)
                    self.__temp = []

                while self.__sep[j] != '\n':
                    self.__temp.append(self.__sep[j])
                    j += 1

                    if j >= len(self.__sep):
                        break

                i = j-1
                j = 0
                self.__file.append(self.__temp)
                self.__temp = []
            else:
                i += 1

        del self.__file[0]
        del self.__temp
        del self.__sep

    def __convert_dict(self):
        list_dest = []
        for i in self.__file[0]:
            list_dest.append(i.rstrip('\n').split(':'))
        self.__dic_destination = dict(list_dest)
        del list_dest
        del self.__file[0]

    def __make_dict(self):
        temp = []
        self.__dict_week_num = []
        for i in range(len(self.__file)):
            step = 0
            while step < len(self.__file[i][0]):
                str1 = self.__file[i][0][step: step + 5].rstrip('\n')
                if str1 != '':
                    str1 = self.__week_dict[str1]
                    temp.append([str1, i])
                step += 5
            del self.__file[i][0]
            del self.__file[i][0]

        self.__dict_week_num = dict(temp)
        del temp

    def __make_list(self):
        filelist = []
        filetemp = []
        for i in range(len(self.__file)):
            for j in self.__file[i]:
                temp = j[3:len(j) - 1]
                filelist.append(temp.split())

            filetemp.append(filelist)
            filelist = []

        self.__file = filetemp
        del temp


if __name__ == "__main__":
    df = nexttrain()
    df.open('kasugano.tbl')

    now = datetime.datetime.today()
    ntrain, trainfo = df.get_time(now)
    delta = ntrain - now
    delta = delta.total_seconds()
    if delta > 3600:
        h = str(ntrain.hour)
        m = str(ntrain.minute)
        text = '次の電車は'+h+'時'+m+'分'+trainfo[:-1]+'ゆきです'
    elif delta > 60:
        text = '次の電車は'+str(int(delta/60))+'分' + \
            str(int(delta % 60))+'秒後'+trainfo[:-1]+'ゆきです'
    else:
        text = '次の電車は'+str(int(delta % 60))+'秒後'+trainfo[:-1]+'ゆきです'
    print(text)
    # clipboard.set(text)
