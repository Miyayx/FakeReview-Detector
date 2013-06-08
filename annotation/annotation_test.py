
import sys
sys.path.append("/home/yang/GraduationProject/utils/")
import fileio

if __name__=="__main__":
    fake1 = fileio.read_file_to_list("mantualdata/annotation_fake1.dat")
    fake2 = fileio.read_file_to_list("mantualdata/annotation_fake2.dat")

    fake1 =list(set(fake1))
    fake2 =list(set(fake2))

    same = []
    for item in fake1:
        if item in fake2:
            same.append(item)
    total = list(set(fake1+fake2))
    print len(same)
    print len(total)

    fileio.record_to_file("../data/target/annotation_fake.dat",total)
