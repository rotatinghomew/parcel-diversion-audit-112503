# 分拣错分归因与在途绕行评估

仓库维护大小件混跑的多来源分拣和接件资料。时钟为班次窗口共用的相对分钟。纸和电子为面单类型。

资料为合成输入。各来源文件的单位、标识及关联见 [资料字典](资料字典.md)。

## 检查资料

使用 Python 3.11。NumPy 与 SciPy 版本在依赖清单中固定。已有环境可直接执行资料检查。首次在本地使用时可以建立虚拟环境并安装依赖。

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

检查只读原始 JSON，报告编号、记录引用、相互关联的原始资料及运行环境是否可用。
