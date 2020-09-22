MapMaker = Class{}

function MapMaker.generate(width, height, bombs)
    local tiles = {}
    local bombTiles = {}

    -- Finding the location of all the bombs as a number, 1 - # of tiles
    bombCounter = 1
    while bombCounter <= bombs do
        bombPlace = math.random(1, width*height)
        isBombCopy = false
        if #bombTiles > 0 then
            for k, bomb in pairs(bombTiles) do
                if bomb == bombPlace then
                    isBombCopy = true
                end
            end
        end
        if not isBombCopy then
            bombTiles[bombCounter] = bombPlace
            bombCounter = bombCounter + 1
        end
    end

    -- creating all of the tiles
    local tileCounter = 1
    for y = 1, height do
        for x = 1, width do
            tiles[tileCounter] = Tile(x, y)
            tileCounter = tileCounter + 1
        end
    end

    -- placing the bombs in the predetermined tiles
    for k, bombIndex in pairs(bombTiles) do
        tiles[bombIndex].bomb = true
    end

    --counting bombs around each tile
    local bombCount
    for k, tile in pairs(tiles) do
        if not tile.bomb then
            bombCount = 0
            for y = math.max(1, tile.y - 1), math.min(tile.y + 1, height) do
                for x = math.max(1, tile.x - 1), math.min(tile.x + 1, width) do
                    if tiles[(y - 1) * width + x].bomb then
                        bombCount = bombCount + 1
                    end
                end
            end
            tile.number = bombCount
        end
    end

    return tiles
end