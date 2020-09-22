

require 'src/Dependencies'

function love.load()
    love.graphics.setDefaultFilter('nearest', 'nearest')
    love.window.setTitle('Minesweeper')

    math.randomseed(os.time())

    push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, {
        fullscreen = false,
        vsync = true,
        resizable = true
    })

    gStateMachine = StateMachine {
        ['start'] = function() return StartState() end,
        ['play'] = function() return PlayState() end
    }

    gStateMachine:change('play')

    mousePress = {}
end

function love.resize(w, h)
    push:resize(w, h)
end

function love.mousepressed(x, y, button, isTouch)
    mousePress = {x, y, button}
end

function love.update(dt)
    gStateMachine:update(dt)
    mousePress = {}
end

function love.draw()
    push:start()
    gStateMachine:render()
    push:finish()
end
