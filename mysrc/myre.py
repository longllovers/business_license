import re
import json
from date_re import extract_time_period

class AdvancedTextCleaner:
    def __init__(self):
        # 基础标签映射
        self.label_map = {
            "统一社会信用代码": ["统一社会信用代码", "注册号", "许可证编号", "社会信用代码", "证书编号"],
            "公司名称": ["公司名称", "名称", "经营者名称", "字号名称", "企业名称"],
            "注册资本": ["注册资本", "资金数额"],
            "法定代表人": ["法定代表人", "法定代表人姓名", "经营者", "法定代表人（负责人）", "经营者姓名", "负责人", "投资人", "企业法定代表人"],
            "地址": ["地址", "住所", "经营场所", "企业住所", "营业场所"],
            "经营范围": ["经营范围", "经营项目", "经营范围及方式"],
            "营业期限": ["营业期限", "执照有效期"],
            "成立日期": ["成立日期", "注册日期"],
            "主体类型": ["商事主体类型","主体类型", "公司类型", "类型", "主体业态", "组成形式", "企业类型", "经济性质", "商事主题类型"]
        }
        
        # 正则优化：构建详细的前缀替换规则
        self.prefix_fixes = {
            "统一社会信用代码": {
                "^\\s*统一社会信用代码\\s*": "",
                "^\\s*统一社会\\s*": "",
                "^\\s*信用代码\\s*": "",
                "^\\s*注册号\\s*": "",
                "^\\s*许可证编号\\s*": "",
                "^\\s*证书编号\\s*": "",
                "^\\s*社会信用代码\\s*": "",
                "^\\s*代码\\s*": "",
                "^\\s*编号\\s*": "",
                "\\s*\\(1-1\\)\\s*":"",
                "\\s*\\(1/1\\)\\s*":"",
                "\\s*\\(7/15\\)\\s*":"",
                "\\s*（1-1）\\s*":"",
            },
            "公司名称": {
                "^\\s*公司名称\\s*": "",
                "^\\s*名称\\s*": "",
                "^\\s*企业名称\\s*": "",
                "^\\s*字号名称\\s*": "",
                "^\\s*经营者名称\\s*": "",
                "^\\s*称\\s*": "",
                "^\\s*名\\s*": "",
                "称\\s+": "",
                "名称\\s+": ""
            },
            "注册资本": {
                "^\\s*注册资本\\s*": "",
                "^\\s*资金数额\\s*": "",
                "^\\s*资本\\s*": "",
                "^\\s*资金\\s*": "",
                "^\\s*资\\s*": "",
                "注册资\\s+": "",
                "资金\\*": "",
                "\\s*注资\\s*":"",
            },
            "法定代表人": {
                "^\\s*法定代表人\\s*": "",
                "^\\s*法定代表人姓名\\s*": "",
                "^\\s*经营者\\s*": "",
                "^\\s*法定代表人（负责人）\\s*": "",
                "^\\s*经营者姓名\\s*": "",
                "^\\s*负责人\\s*": "",
                "^\\s*投资人\\s*": "",
                "^\\s*企业法定代表人\\s*": "",
                "^\\s*法人\\s*": "",
                "^\\s*代表人\\s*": "",
                "^\\s*人\\s*": "",
                "^\\s*姓名\\s*": "",
                "\\s*住所\\s*":"",
            },
            "地址": {
                "^\\s*地址\\s*": "",
                "^\\s*住所\\s*": "",
                "^\\s*经营场所\\s*": "",
                "^\\s*企业住所\\s*": "",
                "^\\s*营业场所\\s*": "",
                "^\\s*所\\s*": "",
                "^\\s*场所\\s*": "",
                "住所\\s+": "",
                "地址\\s+": ""
            },
            "经营范围": {
                "^\\s*经营范围及方式\\s*": "",
                "^\\s*经营范围\\s*": "",
                "^\\s*范围\\s*": "",
                "^\\s*项目\\s*": "",
                "\\s*经营范围\\s*": "",
                "\\s*经营项目\\s*": "",
                "\\s*及方式\\s*": "",
                "\\s*经营范围\\s*": "",
            },
            "营业期限": {
                "^\\s*营业期限\\s*": "",
                "^\\s*执照有效期\\s*": "",
                "^\\s*期限\\s*": "",
                "^\\s*有效期\\s*": "",
                "营业期限\\s+": "",
                "执照有效期\\s+": ""
            },
            "成立日期": {
                "^\\s*成立日期\\s*": "",
                "^\\s*注册日期\\s*": "",
                "^\\s*日期\\s*": "",
                "^\\s*成立\\s*": "",
                "^\\s*注册\\s*": "",
                "成立日期\\s+": "",
                "注册日期\\s+": "",
                "^\\s*期\\s*": "",
                "^\\s*注[\\s\\w\\*]*期\\s*": "", 
            },
            "主体类型": {
                "^\\s*主体类型\\s*": "",
                "^\\s*公司类型\\s*": "",
                "^\\s*类型\\s*": "",
                "^\\s*主体业态\\s*": "",
                "^\\s*组成形式\\s*": "",
                "^\\s*企业类型\\s*": "",
                "^\\s*经济性质\\s*": "",
                "^\\s*商事主题类型\\s*": "",
                "^\\s*型\\s*": "",
                "^\\s*态\\s*": "",
                "主体类型\\s+": "",
                "公司类型\\s+": "",
                "类型\\s+": "",
                "四$":""
            }
        }
        
        # 格式标准化规则
        self.format_rules = {
            "注册资本": self._format_capital,
            "成立日期": self._format_date,
            # 可以添加其他格式化函数
        }

    def _remove_all_prefixes(self, text, field):
        """移除所有可能的前缀"""
        # 首先应用标准的标签移除
        for prefix in self.label_map.get(field, []):
            text = re.sub(f"^{prefix}\\s*", "", text).strip()
        
        # 然后再次正则修复
        if field in self.prefix_fixes:
            for pattern, replacement in self.prefix_fixes[field].items():
                text = re.sub(pattern, replacement, text)
        
        return text.strip()
    
    def _format_capital(self, text):
        """标准化注册资本格式"""
        return text
    
    def _format_date(self, text):
        """标准化日期格式"""

        return text
    
    def clean_text(self, contents):
        """清理文本内容"""
        result = {}
        
        for field in self.label_map.keys():
            if field in contents:
                # 第一步：移除前缀
                cleaned_text = self._remove_all_prefixes(contents[field], field)
                if field in self.format_rules:
                    cleaned_text = self.format_rules[field](cleaned_text)
                
                if field == '营业期限':
                    cleaned_text = extract_time_period(cleaned_text)
                result[field] = cleaned_text.replace('"','')
            # else:
            #     result[field] = ""
        
        return result
    
    def process(self, contents):
        """处理内容并返回JSON字符串"""
        cleaned_data = self.clean_text(contents)
        # return json.dumps(cleaned_data, ensure_ascii=False, indent=4)
        return cleaned_data


# 测试例子
if __name__ == "__main__":
    contents = {
        '经营范围': '纳米材料的研发、加工：玻璃制品的加工：防火玻璃、防弹玻璃经营范围、防火玻璃窗加工、销售：国内贸易。（国家有专项规定的除外涉及许可证的凭许可证经营）***',
        '注册资本': '注册资本伍仟万圆整',
        '地址': '住所福建省福州市台江区宁化街道祥坂街6号（原上浦路南侧）富力商务中心（二区）（富力中心B区）B2#楼16层01商务办公',
        '主体类型': '商事主体类型其他有限责任公司',
        '成立日期': '注舟日期2021年10月22日 ',
        '公司名称': '称 福建省诚信保安服务有限公司',
        '法定代表人': '法定代表人王新民',
        '统一社会信用代码': '91320205MA1YHGA34Q(1/1)',
    }

    cleaner = AdvancedTextCleaner()
    cleaned_contents = cleaner.process(contents)
    
    print("清理结果：")
    for field, content in cleaned_contents.items():
        print(f"{field}: {content}")