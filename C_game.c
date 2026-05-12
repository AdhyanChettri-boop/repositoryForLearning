#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

struct Player {
    char name[50];
    int hp;
    int maxHp;
    int attack;
    int level;
    int xp;
    int gold;
    int potions;
};

struct Enemy {
    char name[50];
    int hp;
    int attack;
    int xpReward;
    int goldReward;
};

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void pauseGame() {
    printf("\nPress ENTER to continue...");
    getchar();
    getchar();
}

void showStats(struct Player p) {
    printf("\n============================\n");
    printf("Player: %s\n", p.name);
    printf("Level : %d\n", p.level);
    printf("HP    : %d/%d\n", p.hp, p.maxHp);
    printf("ATK   : %d\n", p.attack);
    printf("XP    : %d\n", p.xp);
    printf("Gold  : %d\n", p.gold);
    printf("Potion: %d\n", p.potions);
    printf("============================\n");
}

void levelUp(struct Player *p) {
    int needed = p->level * 50;

    if (p->xp >= needed) {
        p->level++;
        p->maxHp += 20;
        p->attack += 5;
        p->hp = p->maxHp;

        printf("\n*** LEVEL UP! ***\n");
        printf("You are now level %d!\n", p->level);
        printf("Max HP increased!\n");
        printf("Attack increased!\n");
    }
}

struct Enemy generateEnemy() {
    struct Enemy e;

    int type = rand() % 4;

    switch(type) {
        case 0:
            strcpy(e.name, "Goblin");
            e.hp = 30;
            e.attack = 5;
            e.xpReward = 20;
            e.goldReward = 10;
            break;

        case 1:
            strcpy(e.name, "Skeleton");
            e.hp = 40;
            e.attack = 7;
            e.xpReward = 30;
            e.goldReward = 15;
            break;

        case 2:
            strcpy(e.name, "Dark Knight");
            e.hp = 60;
            e.attack = 10;
            e.xpReward = 50;
            e.goldReward = 30;
            break;

        default:
            strcpy(e.name, "Dragon");
            e.hp = 100;
            e.attack = 15;
            e.xpReward = 100;
            e.goldReward = 75;
            break;
    }

    return e;
}

void usePotion(struct Player *p) {
    if (p->potions > 0) {
        int heal = 30;

        p->hp += heal;

        if (p->hp > p->maxHp) {
            p->hp = p->maxHp;
        }

        p->potions--;

        printf("\nYou used a potion!");
        printf("\nRecovered %d HP.\n", heal);
    } else {
        printf("\nNo potions left!\n");
    }
}

void battle(struct Player *p) {
    struct Enemy e = generateEnemy();

    printf("\nA wild %s appeared!\n", e.name);

    while (e.hp > 0 && p->hp > 0) {

        printf("\n======================\n");
        printf("%s HP: %d\n", e.name, e.hp);
        printf("%s HP: %d/%d\n", p->name, p->hp, p->maxHp);
        printf("======================\n");

        printf("\n1. Attack");
        printf("\n2. Use Potion");
        printf("\n3. Run");

        printf("\nChoose: ");

        int choice;
        scanf("%d", &choice);

        if (choice == 1) {

            int damage = p->attack + (rand() % 6);

            printf("\nYou hit the %s for %d damage!\n",
                   e.name, damage);

            e.hp -= damage;

        } else if (choice == 2) {

            usePotion(p);

        } else if (choice == 3) {

            int escape = rand() % 2;

            if (escape) {
                printf("\nYou escaped successfully!\n");
                return;
            } else {
                printf("\nEscape failed!\n");
            }

        } else {
            printf("\nInvalid option!\n");
            continue;
        }

        if (e.hp > 0) {

            int enemyDamage = e.attack + (rand() % 5);

            printf("%s attacks for %d damage!\n",
                   e.name, enemyDamage);

            p->hp -= enemyDamage;
        }
    }

    if (p->hp <= 0) {
        printf("\nYou were defeated...\n");
        return;
    }

    printf("\nYou defeated the %s!\n", e.name);

    p->xp += e.xpReward;
    p->gold += e.goldReward;

    printf("Gained %d XP!\n", e.xpReward);
    printf("Found %d gold!\n", e.goldReward);

    if (rand() % 3 == 0) {
        p->potions++;
        printf("You found a potion!\n");
    }

    levelUp(p);
}

void shop(struct Player *p) {

    while (1) {

        printf("\n===== SHOP =====\n");
        printf("Gold: %d\n", p->gold);

        printf("\n1. Buy Potion (20 Gold)");
        printf("\n2. Upgrade Attack (50 Gold)");
        printf("\n3. Leave Shop");

        printf("\nChoose: ");

        int choice;
        scanf("%d", &choice);

        if (choice == 1) {

            if (p->gold >= 20) {
                p->gold -= 20;
                p->potions++;
                printf("\nPotion purchased!\n");
            } else {
                printf("\nNot enough gold!\n");
            }

        } else if (choice == 2) {

            if (p->gold >= 50) {
                p->gold -= 50;
                p->attack += 3;
                printf("\nAttack upgraded!\n");
            } else {
                printf("\nNot enough gold!\n");
            }

        } else if (choice == 3) {

            return;

        } else {

            printf("\nInvalid choice!\n");
        }
    }
}

int main() {

    srand(time(NULL));

    struct Player player;

    clearScreen();

    printf("=================================\n");
    printf("     TERMINAL DUNGEON RPG\n");
    printf("=================================\n");

    printf("\nEnter your hero name: ");
    scanf("%s", player.name);

    player.hp = 100;
    player.maxHp = 100;
    player.attack = 10;
    player.level = 1;
    player.xp = 0;
    player.gold = 50;
    player.potions = 2;

    while (1) {

        printf("\n========== MAIN MENU ==========\n");

        printf("\n1. Explore Dungeon");
        printf("\n2. View Stats");
        printf("\n3. Visit Shop");
        printf("\n4. Exit Game");

        printf("\nChoose: ");

        int choice;
        scanf("%d", &choice);

        switch(choice) {

            case 1:
                battle(&player);

                if (player.hp <= 0) {
                    printf("\nGAME OVER\n");
                    return 0;
                }
                break;

            case 2:
                showStats(player);
                break;

            case 3:
                shop(&player);
                break;

            case 4:
                printf("\nThanks for playing!\n");
                return 0;

            default:
                printf("\nInvalid option!\n");
        }
    }

    return 0;
}
