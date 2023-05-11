font = pygame.font.Font(None, 30)

stat_box = pygame.Rect(300, 300, 200, 200)

hero_box = pygame.Rect(0, 0, 70, 200)

hero_box.topleft = stat_box.topright

data = {
    "level": ["12"],
    "name": ["Strong", "Blade", "Rune"],
    "slot": ["4"],
    "main": ["HP", "+47%"],
    "subs": [
        ["F_Hp", "+312"],
        ["SPD", "+5"],
        ["CRI Rate", "+12%"],
        ["ATK", "+7%"],
        ["CRI Dmg", "+21%"],
    ],
}

stat_data = []

stat_data.append(" ".join(data["main"]))

for lst in data["subs"]:
    stat_data.append(" ".join(lst))

stat_text = font.render("\n\n".join(item for item in stat_data), True, "white")

stat_text_rect = stat_text.get_rect(topleft=(stat_box.left + 10, stat_box.top + 20))


font.align = pygame.FONT_CENTER

roll_eff = [["f_hp", 0], ["spd", 0], ["cri rate", 100], ["atk", 0], ["cri dmg", 200]]

hero_text = font.render("\n\n".join(str(item[1]) for item in roll_eff), True, "white")

hero_text_rect = hero_text.get_rect(top=hero_box.top + 20, centerx=hero_box.centerx)
