
import json
import fileio

def convert_to_json(review_list,rid_target):
    reviews = []
    for rid,content,user,time in review_list:
        rid = eval(rid)
        if rid in rid_target.keys():
            review = {"rid":rid,"review":content,"reviewer":user,"time":time}
            if rid_target[rid]:
                review["fake"] = True
            reviews.append(review)
    return json.dumps(reviews)

if __name__ == "__main__":
    review_list = fileio.read_fields_from_allcsv("/home/yang/GraduationProject/data/CSV/Train/",["id","reviewContent","userNick","reviewTime"])
    rid_target = fileio.read_file_to_list("../data/target/uidemo.dat")

    rids = []
    targets = []
    for item in rid_target:
        items = item.split()
        rids.append(eval(items[0]))
        targets.append(eval(items[1]))

    reviews = []

    for rid,content,user,time in review_list:
        rid = eval(rid)
        if rid in rids:
            index = rids.index(rid)
            review = {"rid":rid,"review":content,"reviewer":user,"time":time}
            if targets[index] == 1:
                review["fake"] = True
            reviews.insert(index,review)

    with open('../data/result/review.json', 'w') as outfile:
      json.dump(reviews, outfile)


