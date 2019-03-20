## Terminal front-end for farkle game

from Game import Player, calculate_score

def yesno(prompt):
    answer = ""
    while answer != "Y" and answer != "N":
        answer = input(prompt).upper()
    return True if answer == "Y" else False


def player_turn(p, target):
    playing = True
    p.start_turn()
    while playing:
        print("--- {name} ---".format(name=p.name))
        print("Current Score: {s}".format(s=p.score))
        print("Turn Score: {s}".format(s=p.turn_score))
        print("Target Score: {s}\n".format(s=target))
        rolls = p.throw_dice()
        if not rolls:
            print("Bust!!")
            break
        dice_num = 1
        dice = list(rolls.items())
        for d, num in dice:
            print("{n}) {d.name}:{num}".format(n=dice_num,
                                               d=d,
                                               num=num))
            dice_num += 1
        got_dice = False
        while not got_dice:
            selected = input("\nPlease enter the dice you wish to select, separated by spaces: ")
            indices = [int(i)-1 for i in selected.split(" ")]
            bad_vals = False
            for i in indices:
                if i < 0 or i > len(dice)-1:
                    bad_vals = True
                    break
            if bad_vals:
                print("Invalid selection!")
                continue
            chosen = [dice[i][0] for i in indices]
            chosen_nums = [dice[i][1] for i in indices]
            if calculate_score(chosen_nums) == 0:
                print("Invalid selection!")
            else:
                print("Selected dice worth {s} points.".format(s=calculate_score(chosen_nums)))
                got_dice = yesno("Confirm selection? (Y/N) ")
        p.score_and_remove(rolls, chosen)

        end = yesno("End turn? (Y/N) ")
        if end:
            playing = False
    p.end_game()
    print("\n{name} ends their turn on {s} points!".format(name=p.name,s=p.score))

def two_player(target=4000):
    p1 = Player("Player 1")
    p2 = Player("Player 2")

    p1.new_game()
    p2.new_game()
    turn = 0 ## player 1's turn
    while p1.score < target and p2.score < target:
        if turn == 0:
            player_turn(p1, target)
            turn = 1
        else:
            player_turn(p2, target)
            turn = 0

    if p1.score > p2.score:
        winner = p1
    else:
        winner = p2
    print("{name} is the winner!".format(name=winner.name))
