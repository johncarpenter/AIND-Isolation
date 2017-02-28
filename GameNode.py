class GameNode:
    """
    Class GameNode

    Holds the value for a single game board state

    Parameters:
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
    """
    def __init__(self, game, move, maximizing=True, depth=1):
        self.depth = depth
        self.game = game
        self.maximizing = maximizing
        self.score = 0
        self.parent = None
        self.children = []
        self.move = move

    def add_child(self,game,move,maximizing=True, depth=1):
        """Adds a child GameNode onto this GameNode as parent

        Parameters:
            depth: int for the depth of the current node

            game : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state

            maximizing_player : bool
                Flag indicating whether the current search depth corresponds to a
                maximizing layer (True) or a minimizing layer (False)
        """
        node = GameNode(game,move,maximizing,depth=depth)
        node.parent = self
        self.children.append(node)
        return node

    def get_best_move(self):
        """After the scoring is completed, this function returns the node with either
        the highest or lowest value based on minimizing Parameters
        Returns:
            move:  tuple(x,y)
        """
        if(len(self.children)==0):
            return (-1,-1)

        scores=[]
        for child in self.children:
            scores.append(child.score)

        #print("Scores {}".format(scores))

        if self.maximizing:
            return self.children[scores.index(max(scores))].move
        else:
            return self.children[scores.index(min(scores))].move

    def populate_children(self):
        """Builds a tree of GameNodes from possible moves
        """
        for move in self.game.get_legal_moves():
            new_game = self.game.forecast_move(move)
            self.add_child(new_game, move, not self.maximizing, self.depth+1)

    def set_child(self,index,child):
        self.children[index] = child

    def dump(self,indent=0):
        print(indent*" ","---Node---")
        print(indent*" ","Depth:{}".format(self.depth))
        print(indent*" ","Maximizing: {}".format(self.maximizing))
        print(indent*" ","Score: {}".format(self.score))
        print(indent*" ","Move: {}".format(self.move))
        print(indent*" ","Possible: {}".format(self.game.get_legal_moves()))

        if(self.children):
            print(indent*" "," --Children({})--".format(len(self.children)))
            for children in self.children:
                children.dump(indent=indent+1)

def score_tree_ab( node, player, alpha=float("-inf"), beta=float("inf"), depth=1, max_depth=3):

    legal_moves = []

    if(depth <= max_depth):
        legal_moves = node.game.get_legal_moves()

    if(len(legal_moves)==0):
        node.score = player.score(node.game,player)
        return node

    if(node.maximizing):
        for move in legal_moves:
            new_game = node.game.forecast_move(move)
            child_node = node.add_child(new_game, move, not node.maximizing, node.depth+1)
            child_node = score_tree_ab(child_node,player,alpha=alpha,beta=beta,depth=depth+1,max_depth= max_depth)
            alpha = max(child_node.score,alpha)
            if(beta <= alpha):
                break
        node.score =  alpha
        return node
    else:
        for move in legal_moves:
            new_game = node.game.forecast_move(move)
            child_node = node.add_child(new_game, move, not node.maximizing, node.depth+1)
            child_node = score_tree_ab(child_node,player,alpha=alpha,beta=beta,depth=depth+1,max_depth= max_depth)
            beta = min(child_node.score , beta)
            if(beta <= alpha):
                break
        node.score =  beta
        return node

def score_tree( node, player,  depth=1, max_depth=3):

    if(depth <= max_depth):
        node.populate_children()

    if(len(node.children)==0):
        node.score = player.score(node.game,player)
        return node

    scores = []
    for child in node.children:
        child_node = score_tree(child, player, depth=depth+1,max_depth = max_depth)
        scores.append(child_node.score)

    node.score = max(scores) if node.maximizing else min(scores)
    return node
