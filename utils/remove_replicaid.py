
import fileio

def remove_replica_id(filename):
    with open(filename,'r') as f:
        ids = fileio.read_file_to_list(filename)
        print "Original length",len(ids)
        ids = set(ids)
        print "Changed length",len(ids)
    fileio.record_to_file(filename,ids)

if __name__ == "__main__":
    remove_replica_id("../data/target/all_fake.dat")
       
