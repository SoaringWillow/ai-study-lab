# 论文骨架 30 篇

每周一篇，按组顺序。综述只用来画地图，**不要代替读原文**。
读完在 `papers/<短名>.md` 里填满 5 问模板，然后在这里打勾。

## 5 问模板

1. 它假设了什么数据？多少 episode、谁采的、什么机器人、场景多样性如何？
2. 动作怎么表示、控制频率多少？离散 token / 连续回归 / diffusion / flow？chunk 多长？
3. 评测在哪跑、多少 trial、有没有置信区间？换个房间还成立吗？
4. 换到我的机器人上，第一个会坏的地方是什么？
5. **如果这个结论是真的，谁的生意会变？**（市场敏锐度的日常训练，不许跳过）

## A 组 · 地基：模仿学习与动作表征

- [ ] ACT / ALOHA
- [ ] Diffusion Policy
- [ ] RT-1
- [ ] Octo
- [ ] OpenVLA

## B 组 · 规模化与数据

- [ ] Open X-Embodiment (RT-X)
- [ ] RT-2
- [ ] DROID
- [ ] BridgeData V2
- [ ] Data Scaling Laws in Imitation Learning for Robotic Manipulation
- [ ] AgiBot World / GO-1
- [ ] RoboMIND

## C 组 · 当代前沿

- [ ] π0
- [ ] π0.5
- [ ] GR00T N1（及 N1.5）
- [ ] Gemini Robotics 1.0 / 1.5
- [ ] RDT-1B
- [ ] 小米 Robotics-0（2026-02 全栈开源，MoE 大脑-小脑）

## D 组 · 世界模型

- [ ] Dreamer V3
- [ ] NVIDIA Cosmos
- [ ] World Action Models: The Next Frontier in Embodied AI（arXiv 2605.12090）
- [ ] real-to-sim 基准（REALM 及 ICLR 2026 相关工作）

## E 组 · 评测与失效

- [ ] LIBERO
- [ ] VLABench
- [ ] RaC — scaling recovery & correction
- [ ] embodiment scaling laws
- [ ] VLA 鲁棒性 / 对抗工作

## 地图 · 四篇综述

- [ ] arXiv 2405.14093 — VLA 综述
- [ ] arXiv 2505.04769 — VLA 概念、进展与挑战
- [ ] arXiv 2507.01925 — action tokenization 视角
- [ ] arXiv 2605.12090 — 世界动作模型
