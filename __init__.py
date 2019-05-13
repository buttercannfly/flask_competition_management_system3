import hello
import re
from hello import *

com_list = Com_info.query.all()
for com_temp in com_list:
    if com_temp.pattern == '个人':
        com_temp.min_p = 1
        com_temp.max_p = 1
        db.session.commit()
    else:
        result = re.findall(r"\d+", string=com_temp.pattern)
        com_temp.min_p = int(result[0])
        com_temp.max_p = int(result[1])
        db.session.commit()
