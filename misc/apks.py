import os
with open('./apk.all') as f:
   apks_dict = {}
   for line in f:
       apks = line.split(',')
       platform = apks[0]
       dir_name = apks[1]
       apk_name = apks[2].strip()
       file_name = os.path.join('/home/jnejati/bperf/apks', dir_name, apk_name)
       if platform not in apks_dict:
           apks_dict[platform] = {}
       apks_dict[platform][apk_name] = (os.path.getsize(file_name)) >> 20
   print(apks_dict)
