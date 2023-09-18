import os
import pandas as pd

waste_list = list()
for i in range(1,5):
        os.chdir("/u/trahman/data/theo/test_2x2_4x2/not_reconstructed/5_sysstems_each_correct/add_0_bs/test/n_" + str(i))
        f = open("times.txt", "w")
        f.close()
        os.system("grep LOOP OUTCAR|awk '{print $7}' >> times.txt ")
        os.system("grep LOOP OUTCAR")
        lines = list()
        with open("times.txt") as file:
                for line in file:
                        line = line.strip()
                        lines.append(line)
        #print(lines)

        for i in range(len(lines)):
                lines[i] = float(lines[i])
        #print(lines)
        waste = (lines[5] - sum(lines[:5])) / lines[5]
        waste_list.append(waste)
        print("%.3f" % waste, "%" )


df = pd.DataFrame()
df["Waste"] = waste_list
df.index = ["1 node", "2 nodes" ,"4 nodes", "8 nodes"]
print(df)
