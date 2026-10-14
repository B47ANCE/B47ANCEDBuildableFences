-- B47ANCE'd Buildable Fences v1.1.0-dev.10
-- Native BuildingObjects are server-phase files (also loaded by SP/clients).
-- Shared-phase requires cannot resolve that directory during initial boot.
require "B47_CohesiveModel"
require "BuildingObjects/ISBuildingObject"
require "BuildingObjects/ISBuildIsoEntity"
local V=B47Cohesive
local originalSprite=ISBuildIsoEntity.getSprite
function ISBuildIsoEntity:getSprite()
    if not V.cursor(self) then return originalSprite(self) end
    if self.B47ChosenFace then self.nSprite=self.B47ChosenFace end
    local face=self:getFace()
    if not face then return nil end
    local tile=face:getTileInfo(0,0,0)
    self.north,self.west=self.nSprite==2,self.nSprite==1
    self.south,self.east=self.nSprite==4,self.nSprite==3
    self.chosenSprite=tile and tile:getSpriteName()
    return self.chosenSprite
end
local originalRotate=ISBuildIsoEntity.rotateKey
function ISBuildIsoEntity:rotateKey(key)
    if not V.cursor(self) or not V.cycle then return originalRotate(self,key) end
    if key==Keyboard.KEY_Q then return V.cycle(self,-1) end
    if key==Keyboard.KEY_E or getCore():isKey(KeybindId.ROTATE_BUILDING,key) then
        return V.cycle(self,1)
    end
end
local originalMouse=ISBuildIsoEntity.rotateMouse
local originalValid=ISBuildIsoEntity.isValid
function ISBuildIsoEntity:isValid(square)
    if V.cursor(self) and not isServer() then
        local cheat=self.character:isBuildCheat() or (ISBuildMenu and ISBuildMenu.cheat)
        if not cheat and not self.buildPanelLogic:canPerformCurrentRecipe() then return false end
    end
    return originalValid(self,square)
end
function ISBuildIsoEntity:rotateMouse(x,y)
    if V.cursor(self) then return end
    return originalMouse(self,x,y)
end
local originalJoypad=ISBuildIsoEntity.onJoypadPressButton
function ISBuildIsoEntity:onJoypadPressButton(index,data,button)
    if V.cursor(self) and V.cycle and (button==Joypad.RBumper or button==Joypad.LBumper) then
        return V.cycle(self,button==Joypad.RBumper and 1 or -1)
    end
    return originalJoypad(self,index,data,button)
end
