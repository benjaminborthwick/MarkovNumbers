

StartState = Class{__includes = BaseState}

function StartState:init()
    self.width = 30
    self.height = 16
    self.bombs = 99
    self.tileMap = MapMaker.generate(self.width, self.height, self.bombs)
end

function StartState:enter() end

function StartState:update(dt)
    if love.keyboard.wasPressed('enter') or love.keyboard.wasPressed('return') then
        gStateMachine:change('play', {
            width = self.width,
            height = self.height,
            bombs = self.bombs,
            tileMap = self.tileMap
        })
    end
end

function StartState:render()
    for k, tile in pairs(self.tileMap) do
        tile:render()
    end
    love.graphics.setFont(gFont)
    love.graphics.setColor(0, 0, 0)
    love.graphics.printf('Press enter to begin', 1, 96, VIRTUAL_WIDTH, 'center')
end

function StartState:exit() end