var SUB_FACTORS = {
  al_1xxx: { power: 0.90, speed: 1.00, note: '纯铝（1系），导热极快，需控制热输入' },
  al_2xxx: { power: 1.05, speed: 0.85, note: '铝铜系（2系），热裂纹敏感，建议脉冲模式' },
  al_3xxx: { power: 0.95, speed: 1.00, note: '铝锰系（3系），焊接性较好' },
  al_4xxx: { power: 0.95, speed: 1.05, note: '铝硅系（4系），流动性好，适合填丝焊' },
  al_5xxx: { power: 1.00, speed: 0.90, note: '铝镁系（5系），最佳焊接性，推荐首选' },
  al_6xxx: { power: 1.00, speed: 1.00, note: '铝镁硅系（6系），常用，需清理氧化层' },
  al_7xxx: { power: 1.10, speed: 0.85, note: '铝锌系（7系），焊接难度大，高温裂纹风险' },
  pure_cu:      { power: 1.00, speed: 1.00, note: '纯铜，高反材料，建议高功率+摆头' },
  brass:        { power: 0.85, speed: 1.10, note: '黄铜，注意锌蒸发，需良好通风' },
  bronze:       { power: 0.90, speed: 1.05, note: '青铜，含锡元素，热裂敏感' },
  phos_bronze:  { power: 0.95, speed: 1.00, note: '磷铜，含磷元素，流动性好但脆性' },
  cupronickel:  { power: 0.90, speed: 1.00, note: '白铜，含镍，焊接性中等' },
};
