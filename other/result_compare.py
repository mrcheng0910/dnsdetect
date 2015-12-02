#!/urs/bin/python
#encoding:utf-8
"""
求DNS两次探测结果的交集、并集、差集
"""
import sys,os,getopt

class SetObj:

    def __init__(self,set_a_path,set_b_path):
        
        try:
            fr_a = open(set_a_path,'r')
            fr_b = open(set_b_path,'r')
        except:
            print 'No such file or directory'
            sys.exit()
        self.set_a = fr_a.readlines()
        self.set_b = fr_b.readlines()
        
        fr_a.close()
        fr_b.close()

    def usage(self):
        """
        输入格式
        """
        print '''
        Usage: result_compare.py [options ...]
        Options:
        -i : the intersection of a and b 
        -u : the union of a and b
        -d : the difference of a and b, b and a
        '''

    def inter_set(self): #两个集合的交集
        return list(set(self.set_a)&set(self.set_b))

    def union_set(self): #两个集合的并集
        return list(set(self.set_a).union(set(self.set_b)))

    def difference_set(self):#两个集合的差集
        return list(set(self.set_a).difference(set(self.set_b))),list(set(self.set_b).difference(set(self.set_a))),

def write2file(set_c=[],filename=''):
    """
    将结果写入文件
    """
    
    if not len(set_c):
        sys.exit()
    fw = open(filename,'w')
    fw.writelines(set_c)
    fw.close()

def main():

    set_c = []
    set_d = []
    try:
        opts, args = getopt.getopt(sys.argv[1:],'iud')  #命令参数
    except getopt.GetoptError:
        usage()
        sys.exit()
    if len(opts) == 0:
        usage()
        sys.exit()
    if not len(args) == 2:
        usage()
        sys.exit()
 
    for opt, arg in opts:

        if opt == '-i':
            set_obj = SetObj(args[0],args[1])
            set_c = set_obj.inter_set()
            write2file(set_c,os.path.basename(args[0])[:-4]+'_inter_' +os.path.basename(args[1])[:-4]) #求交集，命名为两个文件命名

        elif opt == '-u':
            set_obj = SetObj(args[0],args[1])
            set_c = set_obj.union_set()
            write2file(set_c,os.path.basename(args[0])[:-4]+'_union_' +os.path.basename(args[1])[:-4]) #求并集，命名为两个文件命名
            
        elif opt == '-d':
            set_obj = SetObj(args[0],args[1])
            set_c ,set_d= set_obj.difference_set()
            write2file(set_c,os.path.basename(args[0])[:-4]+'_difference_' +os.path.basename(args[1])[:-4]) #求差集，命名为两个文件命名
            write2file(set_d,os.path.basename(args[1])[:-4]+'_difference_' +os.path.basename(args[0])[:-4]) #求差集，命名为两个文件命名

if __name__ == '__main__':
    main()