# 用户资料档案

## 读取时机

首次建档、用户更新简历/作品集、事实发生冲突或岗位需要档案中没有的关键信息时读取本文件。

## JSON 结构

```json
{
  "schema_version": 1,
  "updated_at": "ISO-8601",
  "identity": {
    "display_name": "",
    "contact_private": {},
    "location_private": ""
  },
  "career": {
    "target_roles": [],
    "seniority": "",
    "preferences": [],
    "constraints": [],
    "public_positioning": ""
  },
  "education": [],
  "experiences": [],
  "projects": [],
  "skills": [],
  "evidence_links": [],
  "answer_assets": [],
  "fact_boundaries": [],
  "sensitive_topics": [],
  "gaps": [],
  "open_questions": [],
  "sources": []
}
```

## 经历与项目字段

每条经历或项目尽量包含：

- `organization`、`role`、`employment_type`、`start`、`end`；
- `context`：项目为何存在；
- `responsibilities`：候选人亲自承担什么；
- `actions`：做过哪些可验证动作；
- `results`：数值、统计周期、基线和归因类型；
- `evidence`：文件、页码/幻灯片、链接或用户确认日期；
- `boundaries`：不能扩大成什么；
- `interview_uses`：适合证明哪些岗位能力；
- `confidence`：`confirmed`、`source_only` 或 `needs_confirmation`。

## 资料冲突

不要静默覆盖。把冲突写入 `open_questions`，至少记录：字段、来源 A、来源 B、日期、暂用口径与原因。用户后续确认后再更新。

## 敏感信息

`contact_private`、健康、家庭、证件、精确住址等仅供内部准备。对外答案默认不引用；只有用户明确要求或岗位流程依法需要时，才按最小必要范围使用。

