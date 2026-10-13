-- B47ANCE'd Buildable Fences v1.1.0-dev.3
require "B47_CohesiveModel"
require "BuildingObjects/ISBuildingObject"
require "BuildingObjects/ISBuildIsoEntity"
local C = B47Cohesive
local originalSprite = ISBuildIsoEntity.getSprite
function ISBuildIsoEntity:getSprite()
    if not C.cursor(self) then return originalSprite(self) end
    local face = self:getFace()
    local axis = face and string.upper(face:getFaceName())
    if axis ~= "N" and axis ~= "W" then return nil end
    self.north, self.west = axis == "N", axis == "W"
    self.south,self.east = false,false
    self.chosenSprite = self.objectInfo:getName() == C.gateName and
        C.gateSprites[axis].closed or C.sprites[axis].plain
    return self.chosenSprite
end
local originalRotate = ISBuildIsoEntity.rotateKey
function ISBuildIsoEntity:rotateKey(key)
    if not C.cursor(self) then return originalRotate(self,key) end
    -- Build 42.21 exposes one ROTATE_BUILDING keyboard binding, not a native
    -- reverse binding. Q/E are a scoped cursor adapter, no global keybinds.
    local delta
    if key == Keyboard.KEY_Q then delta = -1
    elseif key == Keyboard.KEY_E then delta = 1
    elseif getCore():isKey(KeybindId.ROTATE_BUILDING,key) then delta = 1 end
    if not delta then return end
    -- Traverse only supported native faces; getFace's forward fallback must
    -- not silently cancel a reverse rotation through absent E/S faces.
    for i=1,4 do
        self.nSprite = ((self.nSprite-1+delta)%4)+1
        local index = self.nSprite == 2 and 0 or (self.nSprite == 4 and 2 or self.nSprite)
        if self.objectInfo:getFace(index) then break end
    end
    self.nSpriteCache = -1
    self:getSprite()
end
local originalMouse = ISBuildIsoEntity.rotateMouse
function ISBuildIsoEntity:rotateMouse(x,y)
    if C.cursor(self) then return end -- held build button must retain chosen axis
    return originalMouse(self,x,y)
end
local originalJoypad = ISBuildIsoEntity.onJoypadPressButton
function ISBuildIsoEntity:onJoypadPressButton(index,data,button)
    if C.cursor(self) and (button == Joypad.RBumper or button == Joypad.LBumper) then
        return self:rotateKey(button == Joypad.RBumper and Keyboard.KEY_E or Keyboard.KEY_Q)
    end
    return originalJoypad(self,index,data,button)
end
