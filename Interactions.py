class Interaction:

    def __init__(self, EBULLETS, BULLETS, playerOne, playerTwo, eList):
        self.EBULLETS = EBULLETS
        self.BULLETS = BULLETS
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.Enemies = eList

        def update(self):
            for bullet in BULLETS():
                for enemy in eList:
                    if bullet.pos == enemy.pos:
                        eList.remove(enemy)  # remove or lower health?
                        EBULLETS.remove(bullet)
                        #increase score
                        KILLED = KILLED + 1 ###

            for bullet in EBULLETS():
                if bullet.pos == playerOne.pos:
                    playerOne.LIVES = playerOne.LIVES - 1
                    BULLETS.remove(bullet)
                elif bullet.pos == playerTwo.pos:
                    playerTwo.LIVES = playerTwo.LIVES - 1
                    BULLETS.remove(bullet)

                if playerOne.LIVES == 0 and playerTwo.LIVES == 0:
                    # Game over screen
                    pass
                elif playerOne.LIVES == 0:
                    # Disable playerOne
                    pass
                elif playerTwo.LIVES == 0:
                    # Disable playerTwo
                    pass

