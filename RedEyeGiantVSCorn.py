import random

def simulate_one(
    D=8,
    time_to_reach=60,
    attack_interval=2.9,
    butter_duration=4,
    p_cannon=0.01,
    p_butter=0.25,
    hp=6000000,
    cannon_damage=1800,
    butter_damage=40,
    corn_damage=20,
    corn_count=1
):
    """
    模拟多株玉米叠种单挑红眼巨人一次。
    参数：
        corn_count : 叠种的玉米数量
    返回 True 表示玉米获胜，False 表示红眼获胜。
    """
    v = D / time_to_reach               # 红眼移动速度（格/秒）
    x = -D                               # 红眼当前位置（玉米在0格）
    frozen_until = 0                      # 定身结束时间，0表示未定身
    last_time = 0                         # 上一次攻击时刻
    next_time = 0                         # 下一次攻击时刻（第一次在0秒）
    total_damage = 0                       # 累计伤害

    while True:
        current_time = next_time
        dt = current_time - last_time

        # 更新红眼位置（考虑定身）
        if dt > 0:
            # 有效移动时间 = max(0, 当前时间 - max(上次事件时间, 定身结束时间))
            move_time = max(0, current_time - max(last_time, frozen_until))
            x += v * move_time

        # 检查红眼是否已走到玉米位置
        if x >= 0:
            return False          # 玉米被吃掉，失败

        # 所有玉米同时攻击
        any_butter = False
        for _ in range(corn_count):
            r = random.random()
            if r < p_cannon:
                total_damage += cannon_damage
            elif r < p_cannon + p_butter:
                total_damage += butter_damage
                any_butter = True      # 至少有一株投出了黄油
            else:
                total_damage += corn_damage

        # 如果本次攻击有黄油，重置定身时间
        if any_butter:
            frozen_until = current_time + butter_duration

        # 检查是否击败红眼
        if total_damage >= hp:
            return True           # 玉米获胜

        # 准备下一次攻击
        last_time = current_time
        next_time += attack_interval

def main():
    corn_count = int(input("请输入玉米叠种的数量: "))
    trial = 0
    while True:
        trial += 1
        if simulate_one(corn_count=corn_count):
            print(f"\n成功！在第 {trial} 次试验中，{corn_count}株玉米投手击败了红眼巨人。")
            break
        if trial % 1000 == 0:
            print(f"已完成 {trial} 次试验...", end='\r')

if __name__ == "__main__":
    main()
