-- B47ANCE'd Buildable Fences v1.1.0-dev.3
-- DEV / RUNTIME TESTING ONLY. Slash adapter + SP native context fallback.
require "B47_FenceTestKitPlan"
require "Chat/ISChat"
local K=B47FenceTestKit
function K.show(player,key,count)
    local message=getText(key,count or 0)
    print(message)
    if player then HaloTextHelper.addText(player,message) end
end
function K.request(player)
    player=player or getSpecificPlayer(0)
    if not player then return end
    if isClient() then
        sendClientCommand(player,"B47FenceTestKit","b47fencetestkit",{})
    elseif K.spawn then K.spawn(player)
    else K.show(player,"IGUI_B47_TestKitFailed") end
end
local original=ISChat.onCommandEntered
function ISChat:onCommandEntered()
    local chat=ISChat.instance or self
    local text=chat.textEntry:getText()
    if text and text:match("^%s*/b47fencetestkit%s*$") then
        chat:logChatCommand("/b47fencetestkit")
        chat:unfocus()
        doKeyPress(false)
        K.request(getSpecificPlayer(0))
        return
    end
    return original(self)
end
Events.OnFillWorldObjectContextMenu.Add(function(playerNum,context,objects,test)
    if test then return end
    context:addOption(getText("IGUI_B47_TestKitMenu"),getSpecificPlayer(playerNum),K.request)
end)
Events.OnServerCommand.Add(function(module,command,args)
    if module ~= "B47FenceTestKit" or command ~= "result" or not args then return end
    local allowed={IGUI_B47_TestKitDenied=true,IGUI_B47_TestKitFailed=true,IGUI_B47_TestKitSpawned=true}
    if allowed[args.key] then K.show(getSpecificPlayer(0),args.key,args.count) end
end)
