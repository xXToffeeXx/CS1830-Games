class Interaction:

    def __init__(self, EBULLETS, BULLETS, playerOne, playerTwo, eList):
        self.E_BULLETS = EBULLETS
        self.BULLETS = BULLETS
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.eList = eList

    def update(self):
            for bullet in BULLETS:
                for enemy in self.eList:
                    if bullet.pos == enemy.pos:
                        self.eList.remove(enemy)  # remove or lower health?
                        BULLETS.remove(bullet)
                        #increase score
                        KILLED = KILLED + 1 ###

            for bullet in E_BULLETS:
                if bullet.pos.y > playerOne.pos.y - 60:
                    if bullet.pos.x > playerOne.pos.x and bullet.pos.x < playerOne.pos.x + 75:
                        if playerOne.LIVES > 0:
                            playerOne.LIVES = playerOne.LIVES - 1
                        E_BULLETS.remove(bullet)
                    elif bullet.pos.x > playerTwo.pos.x and bullet.pos.x < playerTwo.pos.x + 75:
                        if playerTwo.LIVES > 0:
                            playerTwo.LIVES = playerTwo.LIVES - 1
                        E_BULLETS.remove(bullet)

                    if playerOne.LIVES == 0 and playerTwo.LIVES == 0:
                        # Game over screen
                        sys.exit('Both players ran out of lives')
                    elif playerOne.LIVES == 0:
                        # Disable playerOne
                        pass
                    elif playerTwo.LIVES == 0:
                        # Disable playerTwo
                        pass
                print('Player One lives: ' + str(playerOne.LIVES))
                print('Player Two lives: ' + str(playerTwo.LIVES))
