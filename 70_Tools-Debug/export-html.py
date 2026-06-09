from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - optional dependency
    yaml = None


TOP_LEVEL_LABELS = {
    "00_Index": "入口 / Index",
    "10_Basics": "基础概念 / Basics",
    "20_Service-Flows": "业务流程 / Flows",
    "30_Troubleshooting": "排障速查 / Triage",
    "40_Case-Library": "案例库 / Cases",
    "50_Platform-Code": "平台代码 / Code",
    "60_Configuration": "配置方法 / Config",
    "70_Tools-Debug": "工具调试 / Tools",
    "90_Decisions": "决策记录 / ADR",
    "99_Templates": "模板 / Templates",
}

NAV_GROUPING_THRESHOLD = 18
NAV_LANDING_FILENAMES = {"readme.md", "home.md", "index.md"}

NAV_SUBGROUP_LABELS = {
    "40_Case-Library": {
        "ROOT": "总览 / Overview",
        "Registration": "注册 / Registration",
        "SIM": "SIM / Card",
        "Call": "通话 / Call",
        "Supplementary-Service": "补充业务 / SS",
        "Data": "数据 / Data",
        "IMS": "IMS",
        "SMS": "短信 / SMS",
        "Signal": "信号 / Signal",
        "Stability": "稳定性 / Stability",
    },
    "60_Configuration": {
        "ROOT": "配置入口 / Core",
        "Business-Config": "业务配置 / Business",
        "References": "字段映射 / References",
        "OperatorRecords": "运营商记录 / OperatorRecords",
    },
}

NAV_SUBGROUP_ORDER = {
    "40_Case-Library": ["ROOT", "Registration", "SIM", "Call", "Supplementary-Service", "Data", "IMS", "SMS", "Signal", "Stability"],
    "60_Configuration": ["ROOT", "Business-Config", "References", "OperatorRecords"],
}

SEARCH_METADATA_FIELDS = [
    "doc_type",
    "domain",
    "status",
    "quality",
    "rat",
    "feature",
    "platform",
    "layer",
    "symptom",
    "cause",
    "operator",
    "project",
    "chipset",
    "source_log",
    "first_bad_point",
    "confidence",
    "tags",
    "search_tier",
]


CSS = r"""
:root {
  color-scheme: light;
  --page: #edf2f3;
  --paper: #ffffff;
  --paper-2: #f7f9f9;
  --paper-3: #eef4f4;
  --ink: #10171d;
  --ink-soft: #26363d;
  --muted: #607176;
  --faint: #87979b;
  --line: #d4dddf;
  --line-strong: #a9babe;
  --sidebar-bg: #171a1c;
  --sidebar-bg-2: #23282b;
  --sidebar-panel: #202629;
  --sidebar-panel-2: #2a3033;
  --sidebar-line: #343d40;
  --sidebar-ink: #f2eee3;
  --sidebar-muted: #a8b1ad;
  --accent: #007278;
  --accent-2: #b85f24;
  --accent-3: #405b6d;
  --accent-soft: #dff1f1;
  --console: #0b2429;
  --console-2: #112f35;
  --warning-soft: #fff1ca;
  --code-bg: #10171b;
  --code-ink: #edf4ef;
  --shadow: 0 18px 44px rgb(18 38 42 / 0.11);
  --shadow-soft: 0 10px 24px rgb(18 38 42 / 0.07);
  --shadow-tight: 0 8px 18px rgb(18 38 42 / 0.08);
  --radius: 8px;
  --sidebar: 304px;
  --outline: 284px;
  --measure: 1120px;
}

* { box-sizing: border-box; }

[hidden] { display: none !important; }

html {
  scroll-behavior: smooth;
  text-size-adjust: 100%;
}

body {
  margin: 0;
  background:
    linear-gradient(90deg, rgb(7 27 32 / 0.034) 0 1px, transparent 1px 80px),
    linear-gradient(180deg, #fbfcfc 0%, #f2f6f7 38%, var(--page) 100%);
  color: var(--ink);
  font-family: "Aptos", "HarmonyOS Sans SC", "Microsoft YaHei UI", "Microsoft YaHei", "Segoe UI Variable", sans-serif;
  font-size: 16px;
  line-height: 1.72;
  letter-spacing: 0;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

a {
  color: var(--accent);
  text-decoration: none;
  text-underline-offset: 3px;
}

a:hover { text-decoration: underline; }

.skip-link {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 100;
  transform: translateY(-140%);
  padding: 8px 12px;
  border-radius: var(--radius);
  background: var(--ink);
  color: #fff;
}

.skip-link:focus { transform: translateY(0); }

.layout {
  display: grid;
  grid-template-columns: var(--sidebar) minmax(0, 1fr);
  min-height: 100vh;
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: auto;
  padding: 18px 14px 24px;
  color: var(--sidebar-ink);
  background:
    linear-gradient(90deg, rgb(255 255 255 / 0.030) 0 1px, transparent 1px 34px),
    linear-gradient(180deg, var(--sidebar-bg) 0%, var(--sidebar-bg-2) 48%, #151719 100%);
  border-right: 1px solid rgb(255 255 255 / 0.09);
  box-shadow: 12px 0 34px rgb(12 16 18 / 0.18);
  scrollbar-color: #6f7778 transparent;
}

.nav { display: grid; gap: 12px; }

.brand {
  display: grid;
  grid-template-columns: 40px 1fr;
  gap: 11px;
  align-items: center;
  padding: 4px 5px 18px;
  border-bottom: 1px solid var(--sidebar-line);
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border: 1px solid rgb(255 255 255 / 0.18);
  border-radius: 7px;
  background: linear-gradient(135deg, #f0c06a, #c8783f);
  color: #171a1c;
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0;
}

.brand strong {
  display: block;
  color: #f8f1df;
  font-size: 17px;
  line-height: 1.2;
  letter-spacing: 0;
}

.brand span {
  color: #aeb5b0;
  font-size: 12px;
}

.search-wrap {
  position: relative;
  margin: 8px 0 3px;
}

.search-wrap::before {
  content: "";
  position: absolute;
  left: 12px;
  top: 50%;
  width: 12px;
  height: 12px;
  border: 2px solid #d6ddd9;
  border-radius: 50%;
  transform: translateY(-55%);
}

.search-wrap::after {
  content: "";
  position: absolute;
  left: 25px;
  top: 27px;
  width: 8px;
  height: 2px;
  background: #d6ddd9;
  transform: rotate(45deg);
}

.search {
  width: 100%;
  min-height: 44px;
  padding: 9px 12px 9px 38px;
  border: 1px solid #3c4547;
  border-radius: var(--radius);
  background: rgb(255 255 255 / 0.070);
  color: #f7f1df;
  font: inherit;
  font-size: 15px;
  outline: 2px solid transparent;
  outline-offset: 2px;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.07);
}

.search:focus {
  border-color: #c9924d;
  background: rgb(255 255 255 / 0.105);
}

.search::placeholder { color: #aeb8b6; }

.nav-empty {
  margin: 0 2px 8px;
  padding: 8px 10px;
  border: 1px dashed #4a5456;
  border-radius: var(--radius);
  color: #e0b56e;
  font-size: 13px;
}

.nav-section {
  border: 1px solid var(--sidebar-line);
  border-radius: var(--radius);
  background: rgb(255 255 255 / 0.035);
  overflow: hidden;
}

.nav-section[open] {
  background: rgb(255 255 255 / 0.058);
}

.nav-section.is-dense[open] {
  background:
    linear-gradient(180deg, rgb(197 142 72 / 0.055), transparent 120px),
    rgb(255 255 255 / 0.052);
}

.nav-section summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-height: 40px;
  padding: 9px 10px;
  cursor: pointer;
  color: #ead8b8;
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  list-style: none;
}

.nav-section summary::-webkit-details-marker { display: none; }

.nav-section summary::before {
  content: "+";
  display: inline-grid;
  place-items: center;
  width: 18px;
  height: 18px;
  margin-right: 2px;
  border: 1px solid #4a5456;
  border-radius: 4px;
  color: #d5a05d;
  font-size: 12px;
}

.nav-section[open] summary::before { content: "-"; }

.nav-count {
  margin-left: auto;
  color: #9fa9a7;
  font-weight: 700;
}

.nav-section-tools {
  display: grid;
  gap: 7px;
  padding: 0 8px 8px;
}

.nav-section-filter {
  width: 100%;
  min-height: 31px;
  padding: 7px 9px;
  border: 1px solid #3b4547;
  border-radius: 6px;
  background: rgb(10 16 18 / 0.36);
  color: #f3efe3;
  font: inherit;
  font-size: 12px;
  outline: none;
}

.nav-section-filter:focus {
  border-color: #c9924d;
  background: rgb(255 255 255 / 0.095);
}

.nav-section-filter::placeholder { color: #97a4a1; }

.nav-section-hint {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  color: #8e9c99;
  font-size: 10px;
  text-transform: uppercase;
}

.nav-links {
  display: grid;
  gap: 1px;
  padding: 0 6px 9px;
}

.nav-subsection {
  margin: 0 0 5px;
  border: 1px solid rgb(255 255 255 / 0.06);
  border-radius: 6px;
  background: rgb(0 0 0 / 0.105);
  overflow: hidden;
}

.nav-subsection[open] {
  background: rgb(255 255 255 / 0.035);
}

.nav-subsection > summary {
  min-height: 31px;
  padding: 6px 8px;
  color: #d8c9aa;
  font-size: 11px;
  letter-spacing: 0;
  text-transform: none;
}

.nav-subsection > summary::before {
  width: 14px;
  height: 14px;
  border-color: #465255;
  color: #d5a05d;
  font-size: 10px;
}

.nav-subsection[open] > summary::before { content: "-"; }

.nav-sub-count {
  margin-left: auto;
  color: #93a09d;
  font-size: 11px;
  font-weight: 700;
}

.nav-sub-links {
  display: grid;
  gap: 1px;
  padding: 0 4px 5px;
}

.nav-sub-links .nav-link {
  padding: 7px 8px;
}

.nav-link {
  display: grid;
  gap: 1px;
  padding: 8px 10px;
  border-left: 2px solid transparent;
  border-radius: 6px;
  color: #d8dedb;
  line-height: 1.3;
}

.nav-link:hover {
  background: #2b3234;
  color: #f8f1df;
  text-decoration: none;
}

.nav-link.active {
  background: linear-gradient(90deg, rgb(213 160 93 / 0.18), rgb(255 255 255 / 0.070));
  border-left-color: #d5a05d;
  color: #fff4dc;
  box-shadow: inset 0 0 0 1px rgb(255 255 255 / 0.055);
}

.nav-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
  font-weight: 650;
}

.nav-path {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #9aa6a3;
  font-size: 11px;
}

.main { min-width: 0; }

.topbar {
  position: sticky;
  top: 0;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  min-height: 58px;
  padding: 9px 32px;
  border-bottom: 1px solid rgb(20 25 31 / 0.11);
  background: rgb(248 251 251 / 0.92);
  backdrop-filter: blur(16px);
}

.topbar::after {
  content: "";
  position: absolute;
  left: 32px;
  right: 32px;
  bottom: -1px;
  height: 1px;
  background: linear-gradient(90deg, var(--accent-2), rgb(184 95 36 / 0.18), transparent 55%);
}

.topbar-main {
  min-width: 0;
  display: grid;
  gap: 2px;
}

.crumb {
  color: var(--muted);
  font-size: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.crumb::before {
  content: "";
  display: inline-block;
  width: 7px;
  height: 7px;
  margin-right: 8px;
  border-radius: 50%;
  background: var(--accent-2);
  box-shadow: 0 0 0 4px rgb(197 106 35 / 0.12);
}

.topbar-title {
  display: block;
  max-width: min(760px, calc(100vw - var(--sidebar) - 360px));
  overflow: hidden;
  color: var(--ink);
  font-size: 14px;
  font-weight: 780;
  line-height: 1.25;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.updated {
  padding: 5px 10px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  color: var(--muted);
  background: rgb(255 255 255 / 0.88);
  font-size: 12px;
  white-space: nowrap;
}

.content {
  width: min(1560px, calc(100vw - var(--sidebar) - 24px));
  margin: 0 auto;
  padding: 34px 30px 88px;
}

.doc-shell {
  display: grid;
  grid-template-columns: minmax(0, var(--measure)) minmax(236px, var(--outline));
  justify-content: start;
  gap: 40px;
  align-items: start;
}

.doc-shell.no-outline {
  grid-template-columns: minmax(0, var(--measure));
}

article {
  min-width: 0;
  max-width: none;
  padding: 0 0 28px;
  overflow-wrap: break-word;
}

article > p,
article > ul,
article > ol,
article > blockquote {
  max-width: 980px;
}

article > h1:first-of-type {
  position: relative;
  margin: 2px 0 30px;
  padding: 6px 0 20px;
  border-bottom: 2px solid #16232a;
  color: var(--ink);
  font-size: 44px;
  font-weight: 820;
  line-height: 1.12;
  max-width: 1000px;
}

article > h1:first-of-type::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 118px;
  height: 2px;
  background: var(--accent-2);
}

h1, h2, h3, h4 {
  color: var(--ink);
  line-height: 1.28;
  letter-spacing: 0;
}

h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 44px 0 14px;
  padding-top: 20px;
  border-top: 1px solid var(--line);
  font-size: 23px;
  font-weight: 780;
}

h2::before {
  content: "";
  flex: 0 0 auto;
  width: 4px;
  height: 24px;
  border-radius: 4px;
  background: var(--accent-2);
}

h3 {
  margin: 32px 0 10px;
  color: var(--ink-soft);
  font-size: 19px;
  font-weight: 760;
}

h4 {
  margin: 22px 0 8px;
  color: var(--ink-soft);
  font-size: 16px;
  font-weight: 760;
}

p { margin: 10px 0; }

ul, ol {
  padding-left: 24px;
  margin: 10px 0 16px;
}

li { margin: 3px 0; }

li::marker { color: var(--accent-2); }

table {
  display: block;
  width: 100%;
  max-width: 100%;
  margin: 18px 0 26px;
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  border-collapse: collapse;
  background: var(--paper);
  box-shadow: var(--shadow-soft);
}

thead, tbody, tr { width: 100%; }

th, td {
  padding: 9px 12px;
  border: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
  overflow-wrap: anywhere;
}

th {
  background: #e8eeee;
  color: #1d2728;
  font-weight: 780;
  line-height: 1.45;
}

tr:nth-child(even) td { background: rgb(246 249 249 / 0.78); }

code {
  padding: 2px 6px;
  border: 1px solid var(--line);
  border-radius: 5px;
  background: #eef5f5;
  color: #182426;
  font-family: "Cascadia Mono", "JetBrains Mono", Consolas, monospace;
  font-size: 0.91em;
}

pre {
  position: relative;
  overflow: auto;
  margin: 18px 0 26px;
  padding: 44px 18px 18px;
  border: 1px solid #1e3035;
  border-radius: var(--radius);
  background:
    linear-gradient(180deg, #1f3036 0 34px, var(--code-bg) 34px);
  color: var(--code-ink);
  box-shadow: 0 16px 36px rgb(18 38 42 / 0.16);
}

pre::before {
  content: "CODE";
  position: absolute;
  top: 8px;
  left: 12px;
  color: #9eb4ad;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0;
}

pre code {
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  overflow-wrap: normal;
  word-break: normal;
}

.copy-code {
  position: absolute;
  top: 6px;
  right: 8px;
  min-height: 26px;
  padding: 4px 8px;
  border: 1px solid rgb(255 255 255 / 0.18);
  border-radius: 5px;
  background: rgb(255 255 255 / 0.08);
  color: #dcebe5;
  cursor: pointer;
  font: inherit;
  font-size: 12px;
}

.copy-code:hover { background: rgb(255 255 255 / 0.14); }

blockquote {
  margin: 18px 0;
  padding: 13px 16px;
  border-left: 4px solid var(--accent-2);
  border-radius: 0 var(--radius) var(--radius) 0;
  background: var(--warning-soft);
  color: #493516;
}

hr {
  border: 0;
  border-top: 1px solid var(--line);
  margin: 28px 0;
}

img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 18px 0 28px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: #fff;
  box-shadow: 0 16px 34px rgb(22 45 50 / 0.10);
}

.meta {
  margin: 6px 0 26px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
  box-shadow: var(--shadow-soft);
}

.meta summary {
  min-height: 38px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 760;
}

.meta table {
  margin: 0;
  border-width: 1px 0 0;
  border-radius: 0;
}

.source-note {
  margin-top: 42px;
  padding-top: 16px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 13px;
}

.outline {
  position: sticky;
  top: 76px;
  max-height: calc(100vh - 100px);
  overflow: auto;
  padding: 4px 0 4px 18px;
  border-left: 1px solid #c3d0d2;
  scrollbar-color: #9db0b4 transparent;
}

.outline-title {
  margin-bottom: 11px;
  color: var(--ink);
  font-size: 12px;
  font-weight: 820;
  text-transform: uppercase;
  letter-spacing: 0;
}

.outline a {
  display: block;
  margin: 2px 0;
  padding: 5px 0 5px 11px;
  border-left: 2px solid transparent;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.35;
}

.outline a:hover,
.outline a.active {
  border-left-color: var(--accent-2);
  color: var(--ink);
  text-decoration: none;
}

.outline .depth-3 { padding-left: 22px; }
.outline .depth-4 { padding-left: 34px; color: var(--faint); }

.index-hero {
  position: relative;
  margin: 2px 0 28px;
  padding: 32px 0 30px;
  border-bottom: 2px solid #16232a;
}

.index-hero::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 128px;
  height: 2px;
  background: var(--accent-2);
}

.index-hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 34px;
  align-items: end;
}

.index-hero-copy {
  min-width: 0;
}

.index-eyebrow {
  margin: 0 0 8px;
  color: var(--accent);
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0;
}

.index-hero h1 {
  margin: 0 0 10px;
  font-size: 58px;
  line-height: 1.04;
  letter-spacing: 0;
}

.index-hero p {
  max-width: 720px;
  color: var(--muted);
}

.signal-panel {
  min-width: 0;
  padding: 16px;
  border: 1px solid rgb(13 45 52 / 0.20);
  border-radius: var(--radius);
  background:
    linear-gradient(90deg, rgb(255 255 255 / 0.08) 0 1px, transparent 1px 32px),
    linear-gradient(180deg, var(--console-2), var(--console));
  color: #edf6f2;
  box-shadow: 0 18px 42px rgb(18 38 42 / 0.16);
}

.signal-panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgb(255 255 255 / 0.12);
}

.signal-panel-title {
  color: #fff3d9;
  font-size: 13px;
  font-weight: 820;
}

.signal-panel-time {
  color: #a8c2bd;
  font-family: "Cascadia Mono", "JetBrains Mono", Consolas, monospace;
  font-size: 12px;
}

.signal-stack {
  display: grid;
  gap: 9px;
}

.signal-row {
  display: grid;
  grid-template-columns: 92px minmax(0, 1fr) auto;
  gap: 10px;
  align-items: center;
  min-height: 34px;
}

.signal-label {
  color: #cce0dc;
  font-size: 12px;
  font-weight: 740;
}

.signal-meter {
  height: 8px;
  overflow: hidden;
  border-radius: 999px;
  background: rgb(255 255 255 / 0.10);
}

.signal-meter span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #e7b35d, #68b9b5);
}

.signal-value {
  color: #fff8e8;
  font-family: "Cascadia Mono", "JetBrains Mono", Consolas, monospace;
  font-size: 12px;
  font-weight: 760;
}

.signal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 14px;
}

.signal-tags span {
  padding: 4px 7px;
  border: 1px solid rgb(255 255 255 / 0.15);
  border-radius: 999px;
  background: rgb(255 255 255 / 0.07);
  color: #dbece8;
  font-size: 12px;
  font-weight: 700;
}

.quick-links {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin-top: 18px;
}

.quick-links a {
  padding: 8px 12px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--paper);
  color: var(--ink);
  font-weight: 700;
  box-shadow: var(--shadow-tight);
}

.quick-links a:hover {
  border-color: var(--accent-2);
  background: #fff;
  text-decoration: none;
}

.index-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.index-stat {
  min-width: 116px;
  padding: 9px 11px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgb(255 255 255 / 0.78);
  box-shadow: var(--shadow-tight);
}

.index-stat strong {
  display: block;
  color: var(--ink);
  font-size: 20px;
  line-height: 1.1;
}

.index-stat span {
  color: var(--muted);
  font-size: 12px;
}

.index-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  grid-auto-flow: dense;
  gap: 14px;
  margin-top: 24px;
}

.index-section {
  position: relative;
  min-width: 0;
  padding: 16px 16px 15px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgb(255 255 255 / 0.86);
  box-shadow: var(--shadow-tight);
  overflow: hidden;
}

.index-section::before {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-2), rgb(0 114 120 / 0.32), transparent 70%);
}

@media (min-width: 1181px) {
  .index-section:nth-child(1),
  .index-section:nth-child(5) {
    grid-column: span 2;
  }
}

.index-section h2 {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin: 0 0 12px;
  padding: 0;
  border: 0;
  font-size: 17px;
}

.index-section h2::before { display: none; }

.index-section ul {
  display: grid;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}

.index-section li {
  margin: 0;
  padding: 7px 0;
  border-top: 1px solid rgb(211 221 223 / 0.72);
  color: var(--muted);
}

.index-section li:first-child { border-top: 0; }

.index-section a {
  color: var(--ink-soft);
  font-weight: 650;
}

.search-console {
  position: relative;
  margin: 26px 0 30px;
  border: 1px solid #aebfc2;
  border-radius: var(--radius);
  background: rgb(255 255 255 / 0.88);
  box-shadow: 0 22px 54px rgb(18 38 42 / 0.14);
  overflow: hidden;
}

.search-panel {
  position: relative;
  padding: 18px;
  border-bottom: 1px solid rgb(255 255 255 / 0.12);
  background:
    linear-gradient(90deg, rgb(255 255 255 / 0.055) 0 1px, transparent 1px 28px),
    linear-gradient(180deg, var(--console-2) 0%, var(--console) 100%);
  color: #eef6f2;
}

.search-panel::before {
  content: "";
  position: absolute;
  left: 18px;
  right: 18px;
  top: 0;
  height: 3px;
  background: linear-gradient(90deg, #e7b35d, rgb(104 185 181 / 0.55), transparent);
}

.global-search-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 10px;
  align-items: center;
}

.global-search-input,
.filter-field select,
.sort-select {
  width: 100%;
  min-height: 42px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: #fff;
  color: var(--ink);
  font: inherit;
  font-size: 14px;
}

.global-search-input {
  min-height: 48px;
  padding: 10px 14px;
  border-color: rgb(255 255 255 / 0.18);
  background: rgb(255 255 255 / 0.96);
  font-size: 16px;
  box-shadow: inset 0 1px 0 rgb(16 39 44 / 0.08);
}

.global-search-input:focus {
  border-color: #e7b35d;
  box-shadow: 0 0 0 4px rgb(231 179 93 / 0.16);
}

.search-action,
.preset-chip {
  min-height: 40px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: #fff;
  color: var(--ink);
  cursor: pointer;
  font: inherit;
  font-size: 13px;
  font-weight: 760;
}

.search-action {
  min-height: 48px;
  padding: 9px 15px;
  border-color: rgb(255 255 255 / 0.18);
  background: #fff8e8;
}

.search-action:hover,
.preset-chip:hover,
.preset-chip.active {
  border-color: var(--accent-2);
  color: var(--ink);
  background: #fff8e8;
  text-decoration: none;
}

.preset-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.preset-chip {
  padding: 7px 10px;
  border-color: rgb(255 255 255 / 0.16);
  background: rgb(255 255 255 / 0.075);
  color: #edf6f2;
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.08);
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 11px;
  margin-top: 15px;
}

.filter-field {
  display: grid;
  gap: 5px;
}

.filter-field span {
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
}

.search-panel .filter-field span {
  color: #b9d1cc;
}

.filter-field select,
.sort-select {
  padding: 8px 10px;
}

.search-panel .filter-field select {
  border-color: rgb(255 255 255 / 0.16);
  background: rgb(255 255 255 / 0.94);
}

.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  min-height: 28px;
  margin-top: 12px;
}

.filter-token {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border: 1px solid #a9c3c6;
  border-radius: 999px;
  background: #e8f5f5;
  color: var(--ink-soft);
  font-size: 12px;
  font-weight: 700;
}

.filter-token button {
  display: inline-grid;
  place-items: center;
  width: 18px;
  height: 18px;
  padding: 0;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
}

.filter-token button:hover {
  background: #d7e8e9;
  color: var(--ink);
}

.result-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 13px 18px;
  border-bottom: 1px solid var(--line);
  background:
    linear-gradient(180deg, #fbfdfd 0%, #f3f7f7 100%);
}

.result-count {
  color: var(--ink-soft);
  font-size: 14px;
  font-weight: 760;
}

.result-count span {
  color: var(--accent);
}

.search-results {
  display: grid;
  gap: 0;
}

.result-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 14px;
  padding: 17px 18px;
  border-top: 1px solid rgb(211 221 223 / 0.72);
  background: rgb(255 255 255 / 0.68);
}

.result-card:first-child { border-top: 0; }

.result-card:hover {
  background: #ffffff;
  box-shadow: inset 4px 0 0 var(--accent-2);
}

.result-title {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
  color: var(--ink);
  font-size: 17px;
  font-weight: 820;
  line-height: 1.35;
}

.result-title:hover {
  color: var(--accent);
  text-decoration: none;
}

.result-source {
  margin-top: 3px;
  color: var(--faint);
  font-size: 12px;
  overflow-wrap: anywhere;
}

.result-excerpt {
  margin: 9px 0 0;
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
}

.result-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

.result-score {
  align-self: start;
  min-width: 52px;
  padding: 5px 8px;
  border: 1px solid #d7e1e3;
  border-radius: 999px;
  color: var(--muted);
  background: #f4f8f8;
  font-size: 12px;
  font-weight: 800;
  text-align: center;
}

.meta-badge {
  display: inline-flex;
  max-width: 100%;
  padding: 3px 7px;
  border: 1px solid #cbdadd;
  border-radius: 999px;
  background: #f8fbfb;
  color: var(--ink-soft);
  font-size: 12px;
  font-weight: 700;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

.meta-badge.quality-curated {
  border-color: #9dc3a8;
  background: #edf7ef;
  color: #28583b;
}

.meta-badge.quality-imported_reference {
  border-color: #d8c18c;
  background: #fff6d8;
  color: #66491a;
}

.meta-badge.quality-generated,
.meta-badge.quality-template {
  border-color: #b8c5cb;
  background: #eef3f5;
  color: #41545b;
}

.search-empty-state {
  padding: 28px 18px;
  color: var(--muted);
  text-align: center;
}

mark {
  padding: 0 2px;
  border-radius: 3px;
  background: #ffe3a3;
  color: var(--ink);
}

.missing {
  padding: 0 4px;
  border-radius: 4px;
  background: #ffe1df;
  color: #8e1f18;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

a:focus-visible,
button:focus-visible,
summary:focus-visible,
.search:focus-visible,
.global-search-input:focus-visible,
.filter-field select:focus-visible,
.sort-select:focus-visible {
  outline: 2px solid #c56a23;
  outline-offset: 3px;
}

.nav-link,
.outline a,
.quick-links a,
.result-title,
a,
button {
  transition: color 140ms ease, background-color 140ms ease, border-color 140ms ease, opacity 140ms ease;
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}

@media (max-width: 1180px) {
  :root { --outline: 220px; }
  .doc-shell { gap: 24px; }
  .filter-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

@media (max-width: 980px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar {
    position: static;
    height: auto;
    max-height: 46vh;
    box-shadow: none;
  }
  .content {
    width: 100%;
    padding: 20px 16px 64px;
  }
  .doc-shell { grid-template-columns: 1fr; }
  .outline { display: none; }
  .topbar {
    position: static;
    align-items: flex-start;
    flex-direction: column;
  }
  .topbar-title {
    max-width: 100%;
  }
  article { max-width: none; }
  .index-hero-grid {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .signal-panel {
    max-width: 520px;
  }
  .filter-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 560px) {
  html,
  body {
    overflow-x: clip;
  }
  body { font-size: 15px; }
  .sidebar {
    max-height: 42vh;
    padding-bottom: 16px;
  }
  .brand { grid-template-columns: 36px 1fr; }
  .index-hero {
    padding: 24px 0 24px;
  }
  .index-hero h1 { font-size: 34px; }
  .signal-panel {
    display: none;
  }
  .global-search-row,
  .result-card {
    grid-template-columns: 1fr;
  }
  .filter-grid { grid-template-columns: 1fr; }
  .result-toolbar {
    align-items: stretch;
    flex-direction: column;
  }
  .topbar { padding: 10px 16px; }
  article > h1:first-of-type { font-size: 32px; }
  article strong,
  article code {
    overflow-wrap: anywhere;
  }
  table { font-size: 14px; }
}
"""


JS = r"""
const navInput = document.querySelector("[data-search]");
const navLinks = [...document.querySelectorAll("[data-nav-link]")];
const navEmpty = document.querySelector("[data-nav-empty]");
const navSections = [...document.querySelectorAll("[data-nav-section]")];
const navSubsections = [...document.querySelectorAll("[data-nav-subsection]")];
const sectionFilters = [...document.querySelectorAll("[data-section-filter]")];

const applyNavSearch = () => {
  const q = navInput ? navInput.value.trim().toLowerCase() : "";
  const sectionQueries = new Map(
    sectionFilters.map((input) => [input.dataset.group, input.value.trim().toLowerCase()])
  );
  let visibleCount = 0;
  for (const link of navLinks) {
    const text = link.dataset.searchText || "";
    const group = link.dataset.group || "";
    const sectionQ = sectionQueries.get(group) || "";
    const hidden = (q.length > 0 && !text.includes(q)) || (sectionQ.length > 0 && !text.includes(sectionQ));
    link.hidden = hidden;
    if (!hidden) visibleCount += 1;
  }
  for (const subsection of navSubsections) {
    const group = subsection.dataset.group || "";
    const sectionQ = sectionQueries.get(group) || "";
    const subsectionLinks = navLinks.filter((link) => link.closest("[data-nav-subsection]") === subsection);
    const hidden = subsectionLinks.length > 0 && subsectionLinks.every((link) => link.hidden);
    subsection.hidden = hidden;
    if ((q || sectionQ) && !hidden) subsection.open = true;
  }
  for (const section of navSections) {
    const group = section.dataset.group;
    const sectionQ = sectionQueries.get(group) || "";
    const groupLinks = navLinks.filter((link) => link.dataset.group === group);
    const hidden = !sectionQ && groupLinks.every((link) => link.hidden);
    section.hidden = hidden;
    if ((q || sectionQ) && !hidden) section.open = true;
  }
  if (navEmpty) navEmpty.hidden = q.length === 0 || visibleCount > 0;
};

if (navInput) {
  navInput.addEventListener("input", applyNavSearch);
}

for (const input of sectionFilters) {
  input.addEventListener("input", applyNavSearch);
}

applyNavSearch();

const normalize = (value) => String(value ?? "").trim();
const normalizeLower = (value) => normalize(value).toLowerCase();
const textValue = (value) => Array.isArray(value) ? value.join(" ") : normalize(value);
const escapeHtml = (value) => normalize(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#39;");

const fieldLabels = {
  group_label: "目录",
  domain: "业务域",
  doc_type: "类型",
  quality: "质量",
  status: "状态",
  search_tier: "搜索层级",
  platform: "平台",
  rat: "制式",
  layer: "层级",
  confidence: "置信度"
};

const baseDocScore = (doc) => {
  const quality = normalizeLower(doc.quality);
  const docType = normalizeLower(doc.doc_type);
  const status = normalizeLower(doc.status);
  const tier = normalizeLower(doc.search_tier);
  let score = 10;
  if (quality === "curated") score += 12;
  if (quality === "imported_reference") score -= 4;
  if (docType === "case") score += 7;
  if (normalize(doc.first_bad_point)) score += 4;
  if (tier === "main_entry") score += 8;
  if (tier === "case_summary") score += 8;
  if (tier === "supplemental") score -= 8;
  if (tier === "reference_only" || docType === "reference") score -= 30;
  if (tier === "archived_entry" || status === "archived") score -= 40;
  if (status === "summarized_with_log_gap") score -= 8;
  if (normalizeLower(doc.confidence) === "low") score -= 10;
  return score;
};

const scoreDoc = (doc, tokens) => {
  const base = baseDocScore(doc);
  if (!tokens.length) return base;
  const title = normalizeLower(doc.title);
  const source = normalizeLower(doc.source);
  const metadata = normalizeLower([
    doc.domain, doc.doc_type, doc.quality, doc.status, doc.platform, doc.rat,
    doc.layer, doc.feature, doc.symptom, doc.cause, doc.first_bad_point, doc.tags, doc.search_tier
  ].map(textValue).join(" "));
  const text = normalizeLower(doc.search_text || doc.text || "");
  const rawText = normalizeLower(doc.raw_text || "");
  let score = base;
  for (const token of tokens) {
    if (title.includes(token)) score += 42;
    if (source.includes(token)) score += 18;
    if (metadata.includes(token)) score += 26;
    if (text.includes(token)) score += 4;
    if (rawText.includes(token)) score += 1;
  }
  return score;
};

const matchesTokens = (doc, tokens) => {
  if (!tokens.length) return true;
  const haystack = normalizeLower(doc.search_text || [
    doc.title, doc.source, doc.group_label, doc.domain, doc.doc_type, doc.quality,
    doc.status, doc.platform, doc.rat, doc.layer, doc.feature, doc.symptom,
    doc.cause, doc.first_bad_point, doc.search_tier, doc.text, doc.raw_text
  ].map(textValue).join(" "));
  return tokens.every((token) => haystack.includes(token));
};

const matchesField = (doc, field, value) => {
  if (!value) return true;
  const actual = normalizeLower(doc[field]);
  return actual === normalizeLower(value);
};

const makeTokens = (query) => normalizeLower(query).split(/\s+/).filter(Boolean);

const highlight = (value, tokens) => {
  let output = escapeHtml(value);
  for (const token of tokens.filter((item) => item.length >= 2).slice(0, 6)) {
    const escaped = token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    output = output.replace(new RegExp(`(${escaped})`, "ig"), "<mark>$1</mark>");
  }
  return output;
};

const buildExcerpt = (doc, tokens) => {
  const text = normalize(doc.text || doc.excerpt || "");
  if (!text) return "";
  if (!tokens.length) return text.slice(0, 220) + (text.length > 220 ? "..." : "");
  const lower = text.toLowerCase();
  const hit = tokens.map((token) => lower.indexOf(token)).filter((idx) => idx >= 0).sort((a, b) => a - b)[0];
  if (hit === undefined) return text.slice(0, 220) + (text.length > 220 ? "..." : "");
  const start = Math.max(0, hit - 76);
  const end = Math.min(text.length, hit + 190);
  return `${start > 0 ? "..." : ""}${text.slice(start, end)}${end < text.length ? "..." : ""}`;
};

const renderBadge = (label, value) => {
  if (!normalize(value)) return "";
  const safe = normalize(value).replace(/[^a-z0-9_-]+/ig, "_");
  const qualityClass = label === "质量" ? ` quality-${safe}` : "";
  return `<span class="meta-badge${qualityClass}">${escapeHtml(label)}: ${escapeHtml(value)}</span>`;
};

const initSearchApp = async () => {
  const app = document.querySelector("[data-search-app]");
  if (!app) return;

  const input = app.querySelector("[data-global-search]");
  const resultsEl = app.querySelector("[data-search-results]");
  const countEl = app.querySelector("[data-result-count]");
  const activeEl = app.querySelector("[data-active-filters]");
  const sortEl = app.querySelector("[data-sort]");
  const clearBtn = app.querySelector("[data-clear-search]");
  const selects = [...app.querySelectorAll("[data-filter]")];
  const presets = [...app.querySelectorAll("[data-preset]")];

  let docs = [];
  if (Array.isArray(window.KB_SEARCH_INDEX)) {
    docs = window.KB_SEARCH_INDEX;
  } else {
    try {
      const response = await fetch("search-index.json", { cache: "no-store" });
      docs = await response.json();
    } catch {
      resultsEl.innerHTML = "<div class=\"search-empty-state\">搜索索引加载失败。请重新导出 HTML。</div>";
      return;
    }
  }

  const optionCounts = (field) => {
    const counts = new Map();
    for (const doc of docs) {
      const value = normalize(doc[field]);
      if (!value) continue;
      counts.set(value, (counts.get(value) || 0) + 1);
    }
    return [...counts.entries()].sort((a, b) => a[0].localeCompare(b[0], "zh-Hans-CN"));
  };

  for (const select of selects) {
    const field = select.dataset.filter;
    const label = fieldLabels[field] || field;
    const current = select.dataset.initial || "";
    select.innerHTML = `<option value="">全部${escapeHtml(label)}</option>` +
      optionCounts(field).map(([value, count]) => `<option value="${escapeHtml(value)}">${escapeHtml(value)} (${count})</option>`).join("");
    if (current) select.value = current;
  }

  const params = new URLSearchParams(window.location.search);
  input.value = params.get("q") || "";
  for (const select of selects) {
    const value = params.get(select.dataset.filter);
    if (value && [...select.options].some((option) => option.value === value)) {
      select.value = value;
    }
  }
  const sortParam = params.get("sort");
  if (sortParam && [...sortEl.options].some((option) => option.value === sortParam)) {
    sortEl.value = sortParam;
  }

  const readFilters = () => Object.fromEntries(selects.map((select) => [select.dataset.filter, select.value]));

  const updateUrl = () => {
    const next = new URL(window.location.href);
    const query = input.value.trim();
    if (query) next.searchParams.set("q", query);
    else next.searchParams.delete("q");
    for (const [field, value] of Object.entries(readFilters())) {
      if (value) next.searchParams.set(field, value);
      else next.searchParams.delete(field);
    }
    if (sortEl.value !== "relevance") next.searchParams.set("sort", sortEl.value);
    else next.searchParams.delete("sort");
    window.history.replaceState({}, "", next);
  };

  const renderActiveFilters = (filters) => {
    const tokens = [];
    if (input.value.trim()) {
      tokens.push({ field: "q", label: "关键词", value: input.value.trim() });
    }
    for (const [field, value] of Object.entries(filters)) {
      if (value) tokens.push({ field, label: fieldLabels[field] || field, value });
    }
    activeEl.innerHTML = tokens.map((item) =>
      `<span class="filter-token">${escapeHtml(item.label)}: ${escapeHtml(item.value)} <button type="button" data-remove-filter="${escapeHtml(item.field)}" aria-label="移除${escapeHtml(item.label)}">×</button></span>`
    ).join("");
  };

  const render = () => {
    const query = input.value.trim();
    const tokens = makeTokens(query);
    const filters = readFilters();
    let results = docs
      .filter((doc) => matchesTokens(doc, tokens))
      .filter((doc) => Object.entries(filters).every(([field, value]) => matchesField(doc, field, value)))
      .map((doc) => ({ ...doc, score: scoreDoc(doc, tokens) }));

    if (sortEl.value === "title") {
      results.sort((a, b) => normalize(a.title).localeCompare(normalize(b.title), "zh-Hans-CN"));
    } else if (sortEl.value === "path") {
      results.sort((a, b) => normalize(a.source).localeCompare(normalize(b.source), "zh-Hans-CN"));
    } else if (sortEl.value === "quality") {
      const rank = { curated: 0, imported_reference: 1, generated: 2, template: 3 };
      results.sort((a, b) => (rank[normalizeLower(a.quality)] ?? 9) - (rank[normalizeLower(b.quality)] ?? 9) || b.score - a.score);
    } else {
      results.sort((a, b) => b.score - a.score || normalize(a.source).localeCompare(normalize(b.source), "zh-Hans-CN"));
    }

    countEl.innerHTML = `找到 <span>${results.length}</span> / ${docs.length} 篇`;
    renderActiveFilters(filters);

    if (!results.length) {
      resultsEl.innerHTML = "<div class=\"search-empty-state\">没有匹配结果。建议减少筛选条件，或换用平台、业务域、第一坏点关键词。</div>";
      updateUrl();
      return;
    }

    const shown = results.slice(0, 120);
    resultsEl.innerHTML = shown.map((doc) => {
      const badges = [
        renderBadge("目录", doc.group_label),
        renderBadge("业务域", doc.domain),
        renderBadge("类型", doc.doc_type),
        renderBadge("质量", doc.quality),
        renderBadge("搜索层级", doc.search_tier),
        renderBadge("平台", doc.platform),
        renderBadge("制式", doc.rat),
        renderBadge("层级", doc.layer),
        renderBadge("状态", doc.status),
        renderBadge("置信度", doc.confidence)
      ].join("");
      const excerpt = buildExcerpt(doc, tokens);
      return `<article class="result-card">
        <div>
          <a class="result-title" href="${escapeHtml(doc.path)}">${highlight(doc.title, tokens)}</a>
          <div class="result-source">${escapeHtml(doc.source)}</div>
          <p class="result-excerpt">${highlight(excerpt, tokens)}</p>
          <div class="result-meta">${badges}</div>
        </div>
        <div class="result-score">${Math.round(doc.score)}</div>
      </article>`;
    }).join("") + (results.length > shown.length ? `<div class="search-empty-state">已显示前 ${shown.length} 条，请继续加关键词或筛选条件缩小范围。</div>` : "");
    updateUrl();
  };

  const applyPreset = (preset) => {
    if (!preset) return;
    for (const item of preset.split(";").filter(Boolean)) {
      const [field, rawValue] = item.split("=");
      const value = rawValue || "";
      if (field === "q") {
        input.value = value;
        continue;
      }
      const select = selects.find((candidate) => candidate.dataset.filter === field);
      if (select && [...select.options].some((option) => option.value === value)) {
        select.value = value;
      }
    }
    render();
  };

  input.addEventListener("input", render);
  sortEl.addEventListener("change", render);
  clearBtn.addEventListener("click", () => {
    input.value = "";
    for (const select of selects) select.value = "";
    sortEl.value = "relevance";
    render();
  });
  for (const select of selects) select.addEventListener("change", render);
  for (const preset of presets) {
    preset.addEventListener("click", () => applyPreset(preset.dataset.preset || ""));
  }
  activeEl.addEventListener("click", (event) => {
    const button = event.target.closest("[data-remove-filter]");
    if (!button) return;
    const field = button.dataset.removeFilter;
    if (field === "q") input.value = "";
    else {
      const select = selects.find((candidate) => candidate.dataset.filter === field);
      if (select) select.value = "";
    }
    render();
  });

  render();
};

initSearchApp();

for (const pre of document.querySelectorAll("pre")) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "copy-code";
  button.textContent = "Copy";
  button.setAttribute("aria-label", "复制代码");
  button.addEventListener("click", async () => {
    const code = pre.querySelector("code")?.innerText || "";
    try {
      await navigator.clipboard.writeText(code);
      button.textContent = "Copied";
      window.setTimeout(() => { button.textContent = "Copy"; }, 1200);
    } catch {
      button.textContent = "Failed";
      window.setTimeout(() => { button.textContent = "Copy"; }, 1200);
    }
  });
  pre.appendChild(button);
}

const outlineLinks = [...document.querySelectorAll(".outline a[href^='#']")];
const headings = outlineLinks
  .map((link) => document.getElementById(decodeURIComponent(link.getAttribute("href").slice(1))))
  .filter(Boolean);

if ("IntersectionObserver" in window && headings.length) {
  const byId = new Map(outlineLinks.map((link) => [decodeURIComponent(link.getAttribute("href").slice(1)), link]));
  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
    if (!visible) return;
    outlineLinks.forEach((link) => link.classList.remove("active"));
    byId.get(visible.target.id)?.classList.add("active");
  }, { rootMargin: "-12% 0px -72% 0px", threshold: 0.01 });
  headings.forEach((heading) => observer.observe(heading));
}
"""


class Page:
    def __init__(self, src: Path, rel_md: str, rel_html: str, title: str) -> None:
        self.src = src
        self.rel_md = rel_md
        self.rel_html = rel_html
        self.title = title
        self.group = rel_md.split("/", 1)[0] if "/" in rel_md else "Root"


def posix_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def html_rel_from_md_rel(rel_md: str) -> str:
    return str(Path(rel_md).with_suffix(".html")).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip() or fallback
    return fallback


def strip_frontmatter(text: str) -> tuple[str, dict[str, Any]]:
    lines = text.splitlines()
    metadata: dict[str, Any] = {}

    def parse_yaml(block: list[str]) -> dict[str, Any]:
        raw = "\n".join(block).strip()
        if not raw:
            return {}
        if yaml is not None:
            loaded = yaml.safe_load(raw)
            return loaded if isinstance(loaded, dict) else {}
        parsed: dict[str, Any] = {}
        for item in block:
            if ":" in item and not item.startswith(" "):
                key, value = item.split(":", 1)
                parsed[key.strip()] = value.strip()
        return parsed

    if len(lines) >= 3 and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                metadata = parse_yaml(lines[1:idx])
                return "\n".join(lines[idx + 1 :]).lstrip("\n"), metadata

    # Legacy local pattern: H1, blank, frontmatter block. Keep the H1.
    if len(lines) >= 5 and lines[0].startswith("# ") and lines[1].strip() == "" and lines[2].strip() == "---":
        for idx in range(3, len(lines)):
            if lines[idx].strip() == "---":
                metadata = parse_yaml(lines[3:idx])
                kept = [lines[0], ""] + lines[idx + 1 :]
                return "\n".join(kept).lstrip("\n"), metadata

    return text, metadata


def slugify(text: str, used: dict[str, int]) -> str:
    base = re.sub(r"<[^>]+>", "", text)
    base = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", base, flags=re.UNICODE).strip("-").lower()
    if not base:
        base = "section"
    count = used.get(base, 0)
    used[base] = count + 1
    return base if count == 0 else f"{base}-{count + 1}"


def build_target_maps(pages: list[Page]) -> tuple[dict[str, Page], dict[str, Page]]:
    by_rel: dict[str, Page] = {}
    by_base: dict[str, Page] = {}
    for page in pages:
        rel_no_ext = page.rel_md[:-3] if page.rel_md.endswith(".md") else page.rel_md
        by_rel[rel_no_ext] = page
        by_base[Path(page.rel_md).stem] = page
    return by_rel, by_base


def relative_href(from_html: str, to_html: str, fragment: str = "") -> str:
    base = posixpath.relpath(to_html, posixpath.dirname(from_html) or ".")
    return base + (f"#{fragment}" if fragment else "")


def resolve_wiki_target(target: str, current: Page, by_rel: dict[str, Page], by_base: dict[str, Page]) -> tuple[Page | None, str]:
    target = target.strip().replace("\\", "/")
    fragment = ""
    if "#" in target:
        target, fragment = target.split("#", 1)
        fragment = fragment.strip()
    target = target[:-3] if target.endswith(".md") else target

    candidate = target
    if "/" in target or target.startswith("."):
        current_dir = posixpath.dirname(current.rel_md[:-3])
        candidate = posixpath.normpath(posixpath.join(current_dir, target))

    page = by_rel.get(candidate)
    if page is None:
        page = by_base.get(posixpath.basename(target))
    return page, fragment


def format_meta_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "<br>".join(html.escape(str(item)) for item in value)
    if isinstance(value, dict):
        return html.escape(json.dumps(value, ensure_ascii=False))
    return html.escape(str(value))


def render_metadata(metadata: dict[str, Any]) -> str:
    if not metadata:
        return ""
    rows = []
    for key, value in metadata.items():
        rows.append(f"<tr><th>{html.escape(str(key))}</th><td>{format_meta_value(value)}</td></tr>")
    return "<details class=\"meta\"><summary>文档元信息</summary><table>" + "".join(rows) + "</table></details>"


def plain_meta_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(item) for item in value if str(item).strip())
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def normalize_metadata(metadata: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in metadata.items():
        text = plain_meta_value(value).strip()
        if text:
            normalized[str(key)] = text
    return normalized


def plain_text_from_markdown(text: str) -> str:
    text = re.sub(r"```(\w+)?", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(
        r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]",
        lambda match: match.group(2) or match.group(1),
        text,
    )
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^[#>\-\*\s|:]+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_search_body(body_markdown: str, metadata: dict[str, Any]) -> tuple[str, str]:
    doc_type = str(metadata.get("doc_type", "")).strip().lower()
    raw_match = re.search(r"(?m)^##\s+(原始案例内容|原始资料内容|来源记录)\s*$", body_markdown)
    if doc_type == "case" and raw_match:
        return body_markdown[: raw_match.start()], body_markdown[raw_match.start() :]
    return body_markdown, ""


def build_search_entry(
    page: Page,
    body_markdown: str,
    metadata: dict[str, Any],
    toc: list[tuple[int, str, str]],
) -> dict[str, Any]:
    normalized_meta = normalize_metadata(metadata)
    headings = [html.unescape(title) for _, title, _ in toc]
    priority_markdown, raw_markdown = split_search_body(body_markdown, normalized_meta)
    priority_text = plain_text_from_markdown(priority_markdown)
    raw_text = plain_text_from_markdown(raw_markdown)
    body_text = plain_text_from_markdown(body_markdown)
    metadata_text = " ".join(
        f"{field} {normalized_meta.get(field, '')}"
        for field in SEARCH_METADATA_FIELDS
        if normalized_meta.get(field, "")
    )
    search_text = " ".join(
        item
        for item in [
            page.title,
            page.rel_md,
            page.rel_html,
            TOP_LEVEL_LABELS.get(page.group, page.group),
            page_subtitle(page),
            metadata_text,
            " ".join(headings),
            priority_text,
        ]
        if item
    )
    entry: dict[str, Any] = {
        "title": page.title,
        "path": page.rel_html,
        "source": page.rel_md,
        "group": page.group,
        "group_label": TOP_LEVEL_LABELS.get(page.group, page.group),
        "section": page_subtitle(page),
        "headings": headings[:80],
        "excerpt": (priority_text or body_text)[:320],
        "text": (priority_text or body_text)[:12000],
        "raw_text": raw_text[:8000],
        "search_text": search_text[:24000].lower(),
        "metadata": normalized_meta,
    }
    for field in SEARCH_METADATA_FIELDS:
        entry[field] = normalized_meta.get(field, "")
    return entry


def convert_local_markdown_link(url: str, current: Page, by_rel: dict[str, Page], by_base: dict[str, Page]) -> str:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url):
        return url
    if url.startswith("#"):
        return url

    clean = url.replace("\\", "/")
    fragment = ""
    if "#" in clean:
        clean, fragment = clean.split("#", 1)
    if clean.endswith(".md"):
        target = clean[:-3]
        current_dir = posixpath.dirname(current.rel_md[:-3])
        candidate = posixpath.normpath(posixpath.join(current_dir, target))
        page = by_rel.get(candidate) or by_base.get(posixpath.basename(candidate))
        if page is not None:
            return relative_href(current.rel_html, page.rel_html, fragment)
    return url


def image_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None

    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")

    if data.startswith((b"GIF87a", b"GIF89a")) and len(data) >= 10:
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")

    if data.startswith(b"\xff\xd8"):
        idx = 2
        while idx + 9 < len(data):
            if data[idx] != 0xFF:
                idx += 1
                continue
            marker = data[idx + 1]
            idx += 2
            if marker in {0xD8, 0xD9}:
                continue
            if idx + 2 > len(data):
                return None
            size = int.from_bytes(data[idx : idx + 2], "big")
            if size < 2 or idx + size > len(data):
                return None
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                return int.from_bytes(data[idx + 5 : idx + 7], "big"), int.from_bytes(data[idx + 3 : idx + 5], "big")
            idx += size

    if data[:4] == b"RIFF" and data[8:12] == b"WEBP" and len(data) >= 30:
        chunk = data[12:16]
        if chunk == b"VP8X" and len(data) >= 30:
            width = 1 + int.from_bytes(data[24:27], "little")
            height = 1 + int.from_bytes(data[27:30], "little")
            return width, height

    if path.suffix.lower() == ".svg":
        text = data[:2000].decode("utf-8", errors="ignore")
        width = re.search(r'width=["\']([0-9.]+)', text)
        height = re.search(r'height=["\']([0-9.]+)', text)
        if width and height:
            return int(float(width.group(1))), int(float(height.group(1)))
        viewbox = re.search(r'viewBox=["\'][^"\']*?\s([0-9.]+)\s([0-9.]+)["\']', text)
        if viewbox:
            return int(float(viewbox.group(1))), int(float(viewbox.group(2)))

    return None


def image_dimension_attrs(url: str, current: Page) -> str:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url) or url.startswith("#"):
        return ""
    clean = url.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")
    path = (current.src.parent / clean).resolve()
    size = image_dimensions(path)
    if not size:
        return ""
    width, height = size
    if width <= 0 or height <= 0:
        return ""
    return f' width="{width}" height="{height}"'


def render_inline(text: str, current: Page, by_rel: dict[str, Page], by_base: dict[str, Page]) -> str:
    code_parts: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        code_parts.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\u0000CODE{len(code_parts) - 1}\u0000"

    text = re.sub(r"`([^`]+)`", stash_code, text)
    escaped = html.escape(text)

    def wiki_repl(match: re.Match[str]) -> str:
        raw = html.unescape(match.group(1))
        if "|" in raw:
            target, label = raw.split("|", 1)
        else:
            target, label = raw, raw.split("#", 1)[0]
        page, fragment = resolve_wiki_target(target, current, by_rel, by_base)
        label_html = html.escape(label.strip())
        if page is None:
            return f"<span class=\"missing\">{label_html}</span>"
        href = html.escape(relative_href(current.rel_html, page.rel_html, fragment))
        return f"<a href=\"{href}\">{label_html}</a>"

    escaped = re.sub(r"\[\[([^\]]+)\]\]", wiki_repl, escaped)

    def image_repl(match: re.Match[str]) -> str:
        alt = match.group(1)
        original_url = html.unescape(match.group(2))
        url = convert_local_markdown_link(original_url, current, by_rel, by_base)
        dimensions = image_dimension_attrs(original_url, current)
        return f"<img src=\"{html.escape(url)}\" alt=\"{html.escape(alt)}\" loading=\"lazy\" decoding=\"async\"{dimensions}>"

    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_repl, escaped)

    def link_repl(match: re.Match[str]) -> str:
        label = match.group(1)
        url = html.unescape(match.group(2))
        href = convert_local_markdown_link(url, current, by_rel, by_base)
        return f"<a href=\"{html.escape(href)}\">{label}</a>"

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)

    for idx, code_html in enumerate(code_parts):
        escaped = escaped.replace(f"\u0000CODE{idx}\u0000", code_html)
    return escaped


def is_table_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line))


def split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]

    cells: list[str] = []
    current: list[str] = []
    wiki_depth = 0
    code_open = False
    idx = 0
    while idx < len(line):
        if line.startswith("[[", idx) and not code_open:
            wiki_depth += 1
            current.append("[[")
            idx += 2
            continue
        if line.startswith("]]", idx) and wiki_depth > 0 and not code_open:
            wiki_depth -= 1
            current.append("]]")
            idx += 2
            continue

        char = line[idx]
        if char == "`":
            code_open = not code_open
            current.append(char)
        elif char == "|" and wiki_depth == 0 and not code_open:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        idx += 1

    cells.append("".join(current).strip())
    return cells


def render_table(lines: list[str], current: Page, by_rel: dict[str, Page], by_base: dict[str, Page]) -> str:
    header = split_table_row(lines[0])
    rows = [split_table_row(line) for line in lines[2:]]
    output = ["<table><thead><tr>"]
    output.extend(f"<th>{render_inline(cell, current, by_rel, by_base)}</th>" for cell in header)
    output.append("</tr></thead><tbody>")
    for row in rows:
        output.append("<tr>")
        output.extend(f"<td>{render_inline(cell, current, by_rel, by_base)}</td>" for cell in row)
        output.append("</tr>")
    output.append("</tbody></table>")
    return "".join(output)


def render_markdown(text: str, current: Page, by_rel: dict[str, Page], by_base: dict[str, Page]) -> tuple[str, list[tuple[int, str, str]]]:
    body, metadata = strip_frontmatter(text)
    lines = body.splitlines()
    output: list[str] = [render_metadata(metadata)]
    toc: list[tuple[int, str, str]] = []
    used_slugs: dict[str, int] = {}
    idx = 0

    while idx < len(lines):
        line = lines[idx]

        if not line.strip():
            idx += 1
            continue

        fence = re.match(r"^```([A-Za-z0-9_-]*)\s*$", line)
        if fence:
            lang = fence.group(1)
            idx += 1
            code_lines: list[str] = []
            while idx < len(lines) and not lines[idx].startswith("```"):
                code_lines.append(lines[idx])
                idx += 1
            idx += 1 if idx < len(lines) else 0
            class_attr = f" class=\"language-{html.escape(lang)}\"" if lang else ""
            output.append(f"<pre><code{class_attr}>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            raw_title = heading.group(2)
            rendered_title = render_inline(raw_title, current, by_rel, by_base)
            slug = slugify(raw_title, used_slugs)
            toc.append((level, html.escape(raw_title), slug))
            output.append(f"<h{level} id=\"{slug}\">{rendered_title}</h{level}>")
            idx += 1
            continue

        if line.strip() in {"---", "***", "___"}:
            output.append("<hr>")
            idx += 1
            continue

        if idx + 1 < len(lines) and "|" in line and is_table_separator(lines[idx + 1]):
            table_lines = [line, lines[idx + 1]]
            idx += 2
            while idx < len(lines) and lines[idx].strip() and "|" in lines[idx]:
                table_lines.append(lines[idx])
                idx += 1
            output.append(render_table(table_lines, current, by_rel, by_base))
            continue

        if re.match(r"^\s*[-*]\s*", line):
            output.append("<ul>")
            while idx < len(lines) and re.match(r"^\s*[-*]\s*", lines[idx]):
                item = re.sub(r"^\s*[-*]\s*", "", lines[idx])
                output.append(f"<li>{render_inline(item, current, by_rel, by_base)}</li>")
                idx += 1
            output.append("</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            output.append("<ol>")
            while idx < len(lines) and re.match(r"^\s*\d+\.\s+", lines[idx]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[idx])
                output.append(f"<li>{render_inline(item, current, by_rel, by_base)}</li>")
                idx += 1
            output.append("</ol>")
            continue

        if line.startswith(">"):
            quote_lines = []
            while idx < len(lines) and lines[idx].startswith(">"):
                quote_lines.append(lines[idx].lstrip("> "))
                idx += 1
            output.append(f"<blockquote>{render_inline(' '.join(quote_lines), current, by_rel, by_base)}</blockquote>")
            continue

        paragraph = [line.strip()]
        idx += 1
        while idx < len(lines):
            probe = lines[idx]
            if not probe.strip():
                break
            if probe.startswith("#") or probe.startswith("```") or re.match(r"^\s*[-*]\s*", probe) or re.match(r"^\s*\d+\.\s+", probe):
                break
            if idx + 1 < len(lines) and "|" in probe and is_table_separator(lines[idx + 1]):
                break
            paragraph.append(probe.strip())
            idx += 1
        output.append(f"<p>{render_inline(' '.join(paragraph), current, by_rel, by_base)}</p>")

    return "\n".join(part for part in output if part), toc


def page_subtitle(page: Page) -> str:
    parts = page.rel_md.split("/")
    if len(parts) <= 1:
        return "root"
    return "/".join(parts[1:-1]) or parts[0]


def nav_subgroup_key(page: Page) -> str:
    parts = page.rel_md.split("/")
    if len(parts) <= 2:
        return "ROOT"
    return parts[1]


def nav_subgroup_label(group: str, subgroup: str) -> str:
    labels = NAV_SUBGROUP_LABELS.get(group, {})
    return labels.get(subgroup, subgroup)


def nav_subgroup_sort_key(group: str, subgroup: str) -> tuple[int, str]:
    order = NAV_SUBGROUP_ORDER.get(group, [])
    rank = order.index(subgroup) if subgroup in order else len(order) + 1
    return rank, nav_subgroup_label(group, subgroup).lower()


def nav_page_sort_key(page: Page) -> tuple[int, str]:
    filename = page.rel_md.rsplit("/", 1)[-1].lower()
    landing_rank = 0 if filename in NAV_LANDING_FILENAMES else 1
    return landing_rank, page.rel_md.lower()


def render_sidebar(pages: list[Page], active: str, current_rel_html: str) -> str:
    active_group = active.split("/", 1)[0] if active else "00_Index"
    chunks = [
        "<aside class=\"sidebar\">",
        "<nav class=\"nav\" aria-label=\"文档导航\">",
        "<div class=\"brand\"><div class=\"brand-mark\">KB</div><div><strong>Telephony-KB</strong><span>通信知识库 HTML 阅读版</span></div></div>",
        "<label class=\"sr-only\" for=\"kb-search\">搜索文档</label>",
        "<div class=\"search-wrap\"><input id=\"kb-search\" class=\"search\" data-search type=\"search\" name=\"q\" inputmode=\"search\" "
        "placeholder=\"搜索文档或路径\" autocomplete=\"off\" spellcheck=\"false\" aria-label=\"搜索文档\"></div>",
        "<div class=\"nav-empty\" data-nav-empty role=\"status\" hidden>没有匹配的文档</div>",
    ]
    grouped: dict[str, list[Page]] = {}
    for page in pages:
        grouped.setdefault(page.group, []).append(page)

    for group in sorted(grouped.keys()):
        group_label = TOP_LEVEL_LABELS.get(group, group)
        group_id = re.sub(r"\W+", "-", group)
        group_pages = sorted(grouped[group], key=nav_page_sort_key)
        open_attr = " open" if group == active_group or (not active and group == "00_Index") else ""
        is_dense = len(group_pages) >= NAV_GROUPING_THRESHOLD
        section_class = "nav-section is-dense" if is_dense else "nav-section"
        chunks.append(f"<details class=\"{section_class}\" data-nav-section data-group=\"{html.escape(group_id)}\"{open_attr}>")
        chunks.append(
            f"<summary><span>{html.escape(group_label)}</span><span class=\"nav-count\">{len(group_pages)}</span></summary>"
        )
        chunks.append("<div class=\"nav-links\">")

        def render_nav_link(page: Page, subgroup_key: str = "", subgroup_label: str = "") -> str:
            href = html.escape(relative_href(current_rel_html, page.rel_html))
            active_class = " active" if page.rel_html == active else ""
            aria_current = " aria-current=\"page\"" if active_class else ""
            search_text = html.escape(f"{page.title} {page.rel_md} {page_subtitle(page)} {subgroup_label}".lower())
            subgroup_attr = f" data-subgroup=\"{html.escape(subgroup_key)}\"" if subgroup_key else ""
            return (
                f"<a class=\"nav-link{active_class}\" data-nav-link data-group=\"{html.escape(group_id)}\" "
                f"data-search-text=\"{search_text}\"{subgroup_attr} href=\"{href}\"{aria_current}>"
                f"<span class=\"nav-title\">{html.escape(page.title)}</span>"
                f"<span class=\"nav-path\">{html.escape(page_subtitle(page))}</span>"
                "</a>"
            )

        if is_dense:
            chunks.append(
                "<div class=\"nav-section-tools\">"
                f"<input class=\"nav-section-filter\" data-section-filter data-group=\"{html.escape(group_id)}\" "
                f"type=\"search\" inputmode=\"search\" placeholder=\"在 {html.escape(group_label)} 内筛选\" "
                f"aria-label=\"在 {html.escape(group_label)} 内筛选\" autocomplete=\"off\" spellcheck=\"false\">"
                "<div class=\"nav-section-hint\"><span>按子目录分组</span><span>输入即过滤</span></div>"
                "</div>"
            )
            subgrouped: dict[str, list[Page]] = {}
            for page in group_pages:
                subgrouped.setdefault(nav_subgroup_key(page), []).append(page)
            subgroup_keys = sorted(
                subgrouped.keys(),
                key=lambda item: nav_subgroup_sort_key(group, item),
            )
            for subgroup in subgroup_keys:
                subgroup_pages = sorted(subgrouped[subgroup], key=nav_page_sort_key)
                subgroup_label = nav_subgroup_label(group, subgroup)
                subgroup_id = re.sub(r"\W+", "-", f"{group_id}-{subgroup}")
                active_subgroup = any(page.rel_html == active for page in subgroup_pages)
                sub_open = " open" if active_subgroup else ""
                chunks.append(
                    f"<details class=\"nav-subsection\" data-nav-subsection data-group=\"{html.escape(group_id)}\" "
                    f"data-subgroup=\"{html.escape(subgroup_id)}\"{sub_open}>"
                )
                chunks.append(
                    f"<summary><span>{html.escape(subgroup_label)}</span><span class=\"nav-sub-count\">{len(subgroup_pages)}</span></summary>"
                )
                chunks.append("<div class=\"nav-sub-links\">")
                for page in subgroup_pages:
                    chunks.append(render_nav_link(page, subgroup_id, subgroup_label))
                chunks.append("</div></details>")
        else:
            for page in group_pages:
                chunks.append(render_nav_link(page))
        chunks.append("</div></details>")
    chunks.append("</nav>")
    chunks.append("</aside>")
    return "\n".join(chunks)


def render_outline(toc: list[tuple[int, str, str]], current_rel_html: str) -> str:
    visible = [(level, title, slug) for level, title, slug in toc if 2 <= level <= 4]
    if not visible:
        return ""
    chunks = ["<nav class=\"outline\" aria-label=\"当前页目录\">", "<div class=\"outline-title\">当前页</div>"]
    chunks.append("<a href=\"#top\">顶部</a>")
    for level, title, slug in visible:
        chunks.append(f"<a class=\"depth-{level}\" href=\"#{html.escape(slug)}\">{title}</a>")
    chunks.append("</nav>")
    return "\n".join(chunks)


def page_template(
    title: str,
    body_html: str,
    toc: list[tuple[int, str, str]],
    pages: list[Page],
    active: str,
    current_rel_html: str,
    source_rel: str,
    generated_at: str,
) -> str:
    sidebar = render_sidebar(pages, active, current_rel_html)
    outline = render_outline(toc, current_rel_html)
    doc_shell_class = "doc-shell" if outline else "doc-shell no-outline"
    generated_datetime = generated_at.replace(" ", "T")
    group = source_rel.split("/", 1)[0] if "/" in source_rel else source_rel
    group_label = TOP_LEVEL_LABELS.get(group, group)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} - Telephony-KB</title>
  <link rel="stylesheet" href="{html.escape(relative_href(current_rel_html, 'assets/kb.css'))}">
</head>
<body>
  <a class="skip-link" href="#main-content">跳到正文</a>
  <div class="layout" id="top">
    {sidebar}
    <main class="main" id="main-content" tabindex="-1">
      <header class="topbar">
        <div class="topbar-main">
          <div class="crumb">{html.escape(group_label)} / {html.escape(source_rel)}</div>
          <div class="topbar-title">{html.escape(title)}</div>
        </div>
        <time class="updated" datetime="{html.escape(generated_datetime)}">Generated {html.escape(generated_at)}</time>
      </header>
      <div class="content">
        <div class="{doc_shell_class}">
          <article>
{body_html}
            <div class="source-note">Markdown source: <code>{html.escape(source_rel)}</code></div>
          </article>
          {outline}
        </div>
      </div>
    </main>
  </div>
  {('<script src="' + html.escape(relative_href(current_rel_html, 'search-index.js')) + '"></script>') if current_rel_html == "index.html" else ""}
  <script src="{html.escape(relative_href(current_rel_html, 'assets/kb.js'))}"></script>
</body>
</html>
"""


def render_index(pages: list[Page], generated_at: str) -> str:
    sections: dict[str, list[Page]] = {}
    for page in pages:
        sections.setdefault(page.group, []).append(page)

    quick = [
        ("进入 Home", "00_Index/Home.html"),
        ("业务知识地图", "00_Index/业务知识地图.html"),
        ("常用速查", "00_Index/速查.html"),
        ("LTE 注册流程", "20_Service-Flows/Network-Registration/LTE注册流程.html"),
        ("Case Library", "40_Case-Library/README.html"),
    ]
    case_count = len(sections.get("40_Case-Library", []))
    config_count = len(sections.get("60_Configuration", []))
    code_count = len(sections.get("50_Platform-Code", []))

    body = [
        "<section class=\"index-hero\">",
        "<div class=\"index-hero-grid\">",
        "<div class=\"index-hero-copy\">",
        "<p class=\"index-eyebrow\">Android Telephony Field Manual</p>",
        "<h1>Telephony-KB</h1>",
        "<p>面向 Android 通信问题定位的静态阅读版。把流程、案例、平台代码、配置方法和调试技巧放在同一个可筛选入口里。</p>",
        "<div class=\"quick-links\">",
    ]
    for label, href in quick:
        body.append(f"<a href=\"{html.escape(href)}\">{html.escape(label)}</a>")
    body.extend([
        "</div>",
        "<div class=\"index-stats\">",
        f"<div class=\"index-stat\"><strong>{len(pages)}</strong><span>文档页面</span></div>",
        f"<div class=\"index-stat\"><strong>{len(sections)}</strong><span>知识域</span></div>",
        f"<div class=\"index-stat\"><strong>{generated_at}</strong><span>导出时间</span></div>",
        "</div>",
        "</div>",
        "<aside class=\"signal-panel\" aria-label=\"知识库覆盖概览\">",
        "<div class=\"signal-panel-head\"><span class=\"signal-panel-title\">KB Coverage</span><span class=\"signal-panel-time\">STATIC HTML</span></div>",
        "<div class=\"signal-stack\">",
        f"<div class=\"signal-row\"><span class=\"signal-label\">Cases</span><span class=\"signal-meter\"><span style=\"width: {min(100, max(12, case_count))}%\"></span></span><span class=\"signal-value\">{case_count}</span></div>",
        f"<div class=\"signal-row\"><span class=\"signal-label\">Config</span><span class=\"signal-meter\"><span style=\"width: {min(100, max(12, config_count * 2))}%\"></span></span><span class=\"signal-value\">{config_count}</span></div>",
        f"<div class=\"signal-row\"><span class=\"signal-label\">Code</span><span class=\"signal-meter\"><span style=\"width: {min(100, max(12, code_count * 7))}%\"></span></span><span class=\"signal-value\">{code_count}</span></div>",
        "</div>",
        "<div class=\"signal-tags\"><span>Registration</span><span>APN</span><span>CarrierConfig</span><span>NV</span><span>MTK</span><span>UNISOC</span></div>",
        "</aside>",
        "</div>",
        "</section>",
        "<section class=\"search-console\" data-search-app>",
        "<div class=\"search-panel\">",
        "<div class=\"global-search-row\">",
        "<label class=\"sr-only\" for=\"global-search\">搜索知识库</label>",
        "<input id=\"global-search\" class=\"global-search-input\" data-global-search type=\"search\" inputmode=\"search\" autocomplete=\"off\" spellcheck=\"false\" placeholder=\"搜索现象、Cause、平台、运营商、代码路径、第一坏点...\">",
        "<button class=\"search-action\" type=\"button\" data-clear-search>清空</button>",
        "</div>",
        "<div class=\"preset-row\" aria-label=\"快捷筛选\">",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"doc_type=case;group_label=案例库 / Cases\">只看 Case</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"doc_type=case;search_tier=case_summary\">强证据 Case</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"search_tier=supplemental\">补充参考</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"search_tier=reference_only\">仅回溯资料</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"quality=curated\">只看精选</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"quality=imported_reference\">导入资料</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"domain=Registration\">注册问题</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"platform=UNISOC\">UNISOC</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"platform=MTK\">MTK</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"q=第一坏点\">第一坏点</button>",
        "<button class=\"preset-chip\" type=\"button\" data-preset=\"q=CQWeb\">CQWeb</button>",
        "</div>",
        "<div class=\"filter-grid\">",
        "<label class=\"filter-field\"><span>目录</span><select data-filter=\"group_label\"></select></label>",
        "<label class=\"filter-field\"><span>业务域</span><select data-filter=\"domain\"></select></label>",
        "<label class=\"filter-field\"><span>类型</span><select data-filter=\"doc_type\"></select></label>",
        "<label class=\"filter-field\"><span>质量</span><select data-filter=\"quality\"></select></label>",
        "<label class=\"filter-field\"><span>状态</span><select data-filter=\"status\"></select></label>",
        "<label class=\"filter-field\"><span>搜索层级</span><select data-filter=\"search_tier\"></select></label>",
        "<label class=\"filter-field\"><span>平台</span><select data-filter=\"platform\"></select></label>",
        "<label class=\"filter-field\"><span>制式</span><select data-filter=\"rat\"></select></label>",
        "<label class=\"filter-field\"><span>层级</span><select data-filter=\"layer\"></select></label>",
        "<label class=\"filter-field\"><span>置信度</span><select data-filter=\"confidence\"></select></label>",
        "</div>",
        "<div class=\"active-filters\" data-active-filters aria-live=\"polite\"></div>",
        "</div>",
        "<div class=\"result-toolbar\">",
        "<div class=\"result-count\" data-result-count>加载搜索索引...</div>",
        "<label class=\"filter-field\"><span>排序</span><select class=\"sort-select\" data-sort><option value=\"relevance\">相关度优先</option><option value=\"quality\">质量优先</option><option value=\"title\">标题 A-Z</option><option value=\"path\">路径 A-Z</option></select></label>",
        "</div>",
        "<div class=\"search-results\" data-search-results></div>",
        "</section>",
        "<div class=\"index-grid\">",
    ])

    for group in sorted(sections.keys()):
        label = TOP_LEVEL_LABELS.get(group, group)
        group_pages = sorted(sections[group], key=nav_page_sort_key)
        body.append("<section class=\"index-section\">")
        body.append(f"<h2>{html.escape(label)} <span class=\"nav-count\">{len(group_pages)}</span></h2>")
        body.append("<ul>")
        for page in group_pages[:12]:
            body.append(f"<li><a href=\"{html.escape(page.rel_html)}\">{html.escape(page.title)}</a></li>")
        if len(group_pages) > 12:
            body.append(f"<li>还有 {len(group_pages) - 12} 篇，使用左侧导航查看</li>")
        body.append("</ul>")
        body.append("</section>")
    body.append("</div>")

    return page_template(
        title="Index",
        body_html="\n".join(body),
        toc=[],
        pages=pages,
        active="",
        current_rel_html="index.html",
        source_rel="generated index",
        generated_at=generated_at,
    )


def clean_previous_outputs(output_root: Path) -> None:
    manifest = output_root / "_manifest.json"
    if not manifest.exists():
        return
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for rel in data.get("generated_files", []):
        target = (output_root / rel).resolve()
        try:
            target.relative_to(output_root.resolve())
        except ValueError:
            continue
        if target.is_file():
            target.unlink()


def copy_attachments(source_root: Path, output_root: Path, generated: list[str]) -> None:
    attachments = source_root / "attachments"
    if not attachments.exists():
        return
    for src in attachments.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(source_root)
        dst = output_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        generated.append(rel.as_posix())


def export_html(source_root: Path, output_root: Path) -> dict[str, Any]:
    source_root = source_root.resolve()
    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    clean_previous_outputs(output_root)

    md_files = sorted(source_root.rglob("*.md"), key=lambda p: p.relative_to(source_root).as_posix().lower())
    pages: list[Page] = []
    for src in md_files:
        rel_md = posix_rel(src, source_root)
        text = read_text(src)
        title = extract_title(text, src.stem)
        pages.append(Page(src=src, rel_md=rel_md, rel_html=html_rel_from_md_rel(rel_md), title=title))

    by_rel, by_base = build_target_maps(pages)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    generated_files: list[str] = []

    write_text(output_root / "assets" / "kb.css", CSS.strip() + "\n")
    generated_files.append("assets/kb.css")
    write_text(output_root / "assets" / "kb.js", JS.strip() + "\n")
    generated_files.append("assets/kb.js")

    search_index: list[dict[str, Any]] = []
    for page in pages:
        raw = read_text(page.src)
        body_markdown, metadata = strip_frontmatter(raw)
        body_html, toc = render_markdown(raw, page, by_rel, by_base)
        page_html = page_template(
            title=page.title,
            body_html=body_html,
            toc=toc,
            pages=pages,
            active=page.rel_html,
            current_rel_html=page.rel_html,
            source_rel=page.rel_md,
            generated_at=generated_at,
        )
        write_text(output_root / page.rel_html, page_html)
        generated_files.append(page.rel_html)
        search_index.append(build_search_entry(page, body_markdown, metadata, toc))

    index_html = render_index(pages, generated_at)
    write_text(output_root / "index.html", index_html)
    generated_files.append("index.html")

    write_text(output_root / "search-index.json", json.dumps(search_index, ensure_ascii=False, indent=2) + "\n")
    generated_files.append("search-index.json")
    write_text(
        output_root / "search-index.js",
        "window.KB_SEARCH_INDEX = " + json.dumps(search_index, ensure_ascii=False, separators=(",", ":")) + ";\n",
    )
    generated_files.append("search-index.js")

    copy_attachments(source_root, output_root, generated_files)

    manifest = {
        "source_root": str(source_root),
        "output_root": str(output_root),
        "generated_at": generated_at,
        "page_count": len(pages),
        "generated_files": sorted(set(generated_files)),
    }
    write_text(output_root / "_manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest


def main() -> int:
    script_root = Path(__file__).resolve().parent
    default_source = script_root.parent
    default_output = Path(r"F:\Codex\Knowledge\Telephony-HMTL")

    parser = argparse.ArgumentParser(description="Export Telephony-KB Markdown files to static HTML.")
    parser.add_argument("--source", default=str(default_source), help="Markdown source root.")
    parser.add_argument("--output", default=str(default_output), help="HTML output root.")
    args = parser.parse_args()

    manifest = export_html(Path(args.source), Path(args.output))
    print(f"Exported {manifest['page_count']} markdown pages")
    print(f"Output: {manifest['output_root']}")
    print(f"Generated at: {manifest['generated_at']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
