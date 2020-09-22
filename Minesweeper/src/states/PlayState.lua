PlayState = Class{__includes = BaseState}

function PlayState:init()
    self.width = 30
    self.height = 16
    self.bombs = 99
    self.tileMap = MapMaker.generate(self.width, self.height, self.bombs)
end

function PlayState:enter()
end

function PlayState:update()
    -- if the mouse was clicked
    if #mousePress > 0 then
        --syncing mouse position with grid
        local mouseX = 1 + math.floor(mousePress[1] / 32)
        local mouseY = 1 + math.floor(mousePress[2] / 32)
        local mouseTile = (mouseY - 1) * 30 + mouseX

        -- if left click
        if mousePress[3] == 1 then
            self.tileMap[mouseTile].revealed = true
        end
    end

end

function PlayState:render()
    for k, tile in pairs(self.tileMap) do
        tile:render()
    end
end