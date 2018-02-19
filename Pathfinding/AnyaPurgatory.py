def Anya(GridData, StartPoint, EndPoint):
    """
    Find the optimal path between two points on a grid. Returns tuple with each point in the path. Returns False if no path exists.
    Anya implementation based on the paper "Optimal Any-angle Pathfinding in Practice", published in the Journal of Artificial Intelligence Research (JAIR); written by D. Harabor, A. Grastien, D. Öz and V. Aksakalli; 2016.
    """
    #
    # Function variables.
    #

    GridHeight = len(GridData) - 1 # We subtract one because lists start at zero. If we want to reference the right-most coordinate, we would otherwise run into an error (address an index that is one-out-of-bounds).
    GridWidth = len(GridData[0]) - 1
    Interval = namedtuple("Interval", "StartFlag StartPoint EndPoint EndFlag")
    Node = namedtuple("Node", "Interval Root")
    Point = namedtuple("Point", "X Y")
    # Complete set-up of variables "Interval", "Node", and "Point".
    Interval.StartFlag = True
    Interval.StartPoint = Point
    Interval.EndPoint = Point
    Interval.EndFlag = True
    Node.Interval = Interval
    Node.Root = Point
    # Back to regular variables.
    RootHistory = []

    #
    # Sub-functions.
    #

    def FareySequence(N, Descending = False):
        """
        Calculate the Farey Sequence of order N.
        """
        # N needs to be min(Width, Height)
        FareySequence = []
        A, B, C, D = 0, 1, 1, N
        if Descending:
            A, C = 1, N - 1
        FareySequence.append(A, C)
        while (C <= N and not Descending) or (A > 0 and Descending):
            K = int((N + B) / D)
            A, B, C, D = C, D, (K * C - A), (K * D - B)
            FareySequence.append(A, B)
        return FareySequence

    def GenerateSuccessors(Node):
        """
        Generates the successors of an Anya search node.
        """
        def GenerateConeSuccessors(PointOne, PointTwo, Root):
            """
            Generates the successors of a cone search node.
            """
            pass

        def GenerateFlatSuccessors(PointOne, Root):
            """
            Generates the successors of a flat search node.
            """
            pass

        def GenerateStartSuccessors(StartPoint):
            """
            Generates the successors for the start search node.
            """
            # Construct a maximal half-closed interval containing all points observable and to the left of StartPoint. (This does not include the StartPoint itself.)
            LeftStartInterval = []
            if LineOfSight(StartPoint, [0, StartPoint[1]]):
                LeftStartInterval = [True, [0, StartPoint[1]], StartPoint, False]
            else:
                LeftPoints = BresenhamLinePoints(StartPoint, [0, StartPoint[1]])
                for Point, PointIndex in enumerate(LeftPoints):
                    if GridData[Point[1]][Point[0]] == 1:
                        LeftStartInterval = [True, LeftPoints[PointIndex], StartPoint, False]
            # Construct a maximal half-closed interval containing all points observable and to the right of StartPoint. (This does not include the StartPoint itself.)
            RightPoints = BresenhamLinePoints(StartPoint, [GridWidth, StartPoint[1]])
            RightStartInterval = []
            if LineOfSight(StartPoint, [GridWidth, StartPoint[1]]):
                RightStartInterval = [False, StartPoint, [GridWidth, StartPoint[1]], True]
            else:
                RightPoints = BresenhamLinePoints(StartPoint, [GridWidth, StartPoint[1]])
                for Point, PointIndex in enumerate(RightPoints):
                    if GridData[Point[1]][Point[0]] == 1:
                        RightStartInterval = [False, StartPoint, RightPoints[PointIndex], True]
            # Construct a maximal half-closed interval containing all points observable and from the row above StartPoint.
            UpperLeftPoints = BresenhamLinePoints([0, StartPoint[1] + 1], [StartPoint[0], StartPoint[1] + 1])
            UpperRightPoints = BresenhamLinePoints([[StartPoint[0], StartPoint[1] + 1]], [GridWidth, StartPoint[1] + 1])
            if LineOfSight(StartPoint, [0, StartPoint[1]]): # If there is a LOS from the Root to the leftmost point in the upper row.
                UpperStartIntervalLeft = [True, [0, StartPoint[1] + 1]]
            else: # Move left until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperLeftPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalLeft = [True, UpperLeftPoints[PointIndex - 1]]
            if LineOfSight(StartPoint, [GridWidth, StartPoint[1] + 1]): # If there is a LOS from the Root to the rightmost point in the upper row.
                UpperStartIntervalRight = [[GridWidth, StartPoint[1] + 1], True]
            else: # Move right until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperRightPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalRight = [UpperRightPoints[PointIndex - 1], True]
            UpperStartInterval = UpperStartIntervalLeft + UpperStartIntervalRight
            # Construct a maximal half-closed interval containing all points observable and from the row below StartPoint.
            LowerLeftPoints = BresenhamLinePoints([0, StartPoint[1] - 1], [StartPoint[0], StartPoint[1] - 1])
            UpperRightPoints = BresenhamLinePoints(StartPoint, [GridWidth, StartPoint[1] + 1])
            if LineOfSight(StartPoint, [0, StartPoint[1]]): # If there is a LOS from the Root to the leftmost point in the lower row.
                UpperStartIntervalLeft = [True, [0, StartPoint[1] + 1]]
            else: # Move left until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperLeftPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalLeft = [True, UpperLeftPoints[PointIndex - 1]]
            if LineOfSight(StartPoint, [GridWidth, StartPoint[1] + 1]): # If there is a LOS from the Root to the rightmost point in the lower row.
                UpperStartIntervalRight = [[GridWidth, StartPoint[1] + 1], True]
            else: # Move right until we no longer have a LOS.
                for Point, PointIndex in enumerate(UpperRightPoints):
                    if not LineOfSight(StartPoint, Point):
                        UpperStartIntervalRight = [UpperRightPoints[PointIndex - 1], True]
            UpperStartInterval = UpperStartIntervalLeft + UpperStartIntervalRight
            # Split each interval at any corner points.
            Intervals = [SplitInterval(LeftStartInterval), SplitInterval(RightStartInterval), SplitInterval(UpperStartInterval), SplitInterval(LowerStartInterval)]
            Log("Anya Intervals for Root {0} created at {1}".format(Root, Intervals), 0)
            Root = StartPoint # The root for all of the StartSuccessors is the StartPoint.
            StartSuccessors = [GenerateSuccessors((Root, Interval)) for Interval in Intervals]
            return StartSuccessors

        if NodeType(Node) == "CONE":
            Successors = GenerateConeSuccessors(Node[0][1], Node[0][-2], Node[1])
        elif NodeType(Node) == "FLAT":
            Succesors = GenerateFlatSuccessors(Node[0][1], Node[1])
        elif NodeType(Node) == "START":
            Successors = GenerateStartSuccessors(Node[0][1:-1])
        return Successors

    def LiesWithin(Point, Interval):
        """
        Determines whether a point lies within an interval.
        """
        IntervalPoints = BresenhamLinePoints(Interval.StartPoint, Interval.EndPoint)
        

    def LineOfSight(PointOne, PointTwo):
        """
        Determines whether two points have a line-of-sight; that is, if a line drawn between them does not intersect with any solid (non-traversable) points.
        """
        LinePoints = BresenhamLinePoints(PointOne, PointTwo)
        
        if any(GridData[Point[1]][Point[0]] for Point in LinePoints) == 1:
            return False
        else:
            return True

    def NodeType(Node):
        """
        Determines and returns the type of an Anya search node.
        """
        Interval, Root = Node
        if Root == [-1, -1]: # If the root of the node is off the map.
            return "START"
        elif Root[1] != Interval[1][1] and Root[1] != Interval[-2][1]: # If the root of the node is not on the same line (does not have the same Y value) as the points contained in the Interval.
            return "CONE"
        elif Root[1] == Interval[1][1] and Root[1] == Interval[-2][1]: # If the root of the node is on the same line as the (has the same Y value) as the points contained in the Interval.
            return "FLAT"

    def ProjectNode(Node):
        """
        Computes and returns the maximum observable interval projection for the node passed.
        If the projection is invalid, returns False.
        """
        if NodeType(Node) == "FLAT":
            pass
        elif NodeType(Node) == "CONE":
            Interval, Root = Node
            if EndPoint[1] > Root[1]: # Project up, because the EndPoint is above the root.
                pass
            elif EndPoint[1] < Root[1]: # Project down, because the EndPoint is below the root.
                pass

    def ShouldPrune(Node):
        """
        Determines whether an Anya search node should be pruned.
        """
        def IsCulDeSac(Node):
            """
            Determines if an Anya search node is a "Cul De Sac".
            """
            for Point in Node[1:-1]:
                if not LineOfSight(Point, Root):
                    return False
            return True

        def IsIntermediate(Node):
            """
            Determines if an Anya search node is an intermediate node.
            """
            return False

        if IsCulDeSac(Node) or IsIntermediate(Node):
            return True
        else:
            return False # Redundant, but explicit! :)

    def SplitInterval(Interval):
        """
        Split an interval at corner points. Return the list of newly created intervals.
        """
        Intervals = []
        return Intervals

    #
    # Mainline function code.
    #

    StepPathData = []
    StartInterval = Interval() # True = Closed, False = Open
    StartRoot = [-1, -1]
    Open = [[StartInterval, StartRoot]] # The start search node's root is located off the grid.
    while Open is not None:
        [Interval, Root] = Open.pop()
        if EndPoint LiesWithin(Interval)
            return PathTo(Interval)
        for [Interval, Root] in GenerateSuccessors([Interval, Root]):
            if not ShouldPrune([Interval, Root]): # Successor pruning.
                Open = set().union([Open, [[Interval, Root]]])
    return StepPathData