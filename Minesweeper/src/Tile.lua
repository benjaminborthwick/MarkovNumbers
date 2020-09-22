Tile = Class{}

function Tile:init(x, y)
    self.x = x
    self.y = y

    self.width = 32
    self.height = 32

    self.bomb = false
    self.flag = false
    self.revealed = false

    self.number = 0
end

function Tile:render()
    if self.revealed then
        if self.bomb then
            love.graphics.draw(gSheet, gFrames['tiles'][6], (self.x - 1) * 32, (self.y - 1) * 32)
        else
            love.graphics.draw(gSheet, gFrames['numbers'][1], (self.x - 1) * 32, (self.y - 1) * 32)
        end
    else
        love.graphics.draw(gSheet, gFrames['tiles'][1], (self.x - 1) * 32, (self.y - 1) * 32)
    end
end