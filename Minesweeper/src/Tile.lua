Tile = Class{}

function Tile:init(x, y)
    self.x = x
    self.y = y

    self.width = 32
    self.height = 32

    self.bomb = false
    self.flag = false
    self.revealed = false
    self.exploded = false

    self.number = 0
end

function Tile:render()
    if self.exploded then
        love.graphics.draw(gSheet, gFrames['tiles'][2], (self.x - 1) * 32, (self.y - 1) * 32)
    elseif self.revealed then
        if self.bomb then
            love.graphics.draw(gSheet, gFrames['tiles'][6], (self.x - 1) * 32, (self.y - 1) * 32)
        else
            love.graphics.draw(gSheet, gFrames['numbers'][self.number + 1], (self.x - 1) * 32, (self.y - 1) * 32)
        end
    else
        if self.flag then
            love.graphics.draw(gSheet, gFrames['tiles'][3], (self.x - 1) * 32, (self.y - 1) * 32)
        else
            love.graphics.draw(gSheet, gFrames['tiles'][1], (self.x - 1) * 32, (self.y - 1) * 32)
        end
    end
end