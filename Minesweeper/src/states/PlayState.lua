PlayState = Class{__includes = BaseState}

function PlayState:enter(params)
    self.width = params.width
    self.height = params.height
    self.bombs = params.bombs
    self.tileMap = params.tileMap
end

function PlayState:update()
    -- if the mouse was clicked
    if #mousePress > 0 then
        --syncing mouse position with grid
        local mouseX = 1 + math.floor(mousePress[1] / 32)
        local mouseY = 1 + math.floor(mousePress[2] / 32)
        local mouseTile = (mouseY - 1) * self.width + mouseX

        -- if left click
        if mousePress[3] == 1 and not self.tileMap[mouseTile].flag then
            self:revealTile(self.tileMap[mouseTile])
        end

        -- if right click
        if mousePress[3] == 2 and self.tileMap[mouseTile].revealed == false then
            self.tileMap[mouseTile].flag = true
        end
    end
end

function PlayState:revealTile(tile)
    tile.revealed = true
    if tile.bomb then
        tile.exploded = true
    elseif tile.number == 0 then
        for y = math.max(1, tile.y - 1), math.min(tile.y + 1, self.height) do
            for x = math.max(1, tile.x - 1), math.min(tile.x + 1, self.width) do
                if not self.tileMap[(y - 1) * self.width + x].revealed and not (y == tile.y and x == tile.x) then
                    self:revealTile(self.tileMap[(y - 1) * self.width + x])
                end
            end
        end
    end
end

function PlayState:render()
    for k, tile in pairs(self.tileMap) do
        tile:render()
    end
end