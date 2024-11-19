from player import Player

class MinMaxAIPlayer(Player): # Inherit from the Player class

    def choose_card_to_play(self, lead_suit):
        # Implement AI-specific decision logic here

        # MinMax Pseodo code
        # MinMax (GamePosition game)
        # {
        #     return MaxMove (game);
        # }
        # 
        # MaxMove (GamePosition game)
        # {
        #     if (GameEnded(game))
        #     {
        #         return EvalGameState(game);
        #     }
        #     else
        #     {
        #         best_move <- {};
        #         moves <- GenerateMoves(game);
        #         ForEach moves
        #         {
        #             move <- MinMove(ApplyMove(game));
        #             if (Value(move) > Value(best_move))
        #             {
        #                 best_move <- move;
        #             }
        #         }
        #         return best_move;
        #     }
        # }
        # 
        # MinMove (GamePosition game)
        # {
        #     best_move <- {};
        #     moves <- GenerateMoves(game);
        #     ForEach moves
        #     {
        #         move <- MaxMove(ApplyMove(game));
        #         if (Value(move) > Value(best_move))
        #         {
        #             best_move <- move;
        #         }
        #     }
        #     return best_move;
        # }

        return super().choose_card_to_play(lead_suit) # change this later