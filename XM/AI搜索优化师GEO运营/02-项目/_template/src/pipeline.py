# -*- coding: utf-8 -*-
"""PXX 端到端编排：一条命令跑完所有模块"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 50)
    print("PXX Pipeline 启动")
    print("=" * 50)
    # TODO: 依次调用各模块
    print("PXX 完成 [OK]")

if __name__ == "__main__":
    main()
