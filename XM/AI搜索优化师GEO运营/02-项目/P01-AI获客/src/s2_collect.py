# -*- coding: utf-8 -*-
"""S2 采集：从数据源抽取线索

当前用"模拟采集器"从 S1 生成的本地 JSON 抽取。
预留了真实爬虫接口桩 scrape_google_maps()，以后要接真实源只需实现该函数。
"""
import json
import os

class BaseScraper:
    """采集器基类：定义统一接口"""
    def collect(self, *args, **kwargs):
        raise NotImplementedError

class MockDirectoryScraper(BaseScraper):
    """模拟名录采集器：读 S1 生成的 JSON，抽取为目标线索"""
    def __init__(self, source_file):
        self.source_file = source_file

    def collect(self):
        with open(self.source_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
        leads = []
        for r in raw:
            leads.append({
                "raw_id": r["id"],
                "company": r["name"],
                "industry": r["industry"],
                "city": r["city"],
                "scale": r["scale"],
                "email": r["email"],
                "phone": r["phone"],
                "website": r["website"],
                "source": "mock_directory",
            })
        return leads

# ---- 真实爬虫接口桩（以后接真实源时实现，替换 MockDirectoryScraper）----
class GoogleMapsScraper(BaseScraper):
    """真实爬虫桩：演示扩展点，未实现具体抓取逻辑"""
    def __init__(self, query, max_results):
        self.query, self.max_results = query, max_results
    def collect(self):
        # 真实实现参考：omkarcloud/google-maps-scraper 等开源项目
        raise NotImplementedError("真实爬虫待接入（当前项目用模拟数据）")

def run(source_file, out_path):
    scraper = MockDirectoryScraper(source_file)
    leads = scraper.collect()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    return len(leads)

if __name__ == "__main__":
    from config import RAW_FILE, LEADS_FILE
    n = run(RAW_FILE, LEADS_FILE)
    print(f"S2 完成：抽取 {n} 条线索 -> {LEADS_FILE}")
