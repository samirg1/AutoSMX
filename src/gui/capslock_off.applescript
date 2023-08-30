ObjC.import("IOKit");
ObjC.import("CoreServices");

(() => {
    const ioConnect = Ref();
    $.IOServiceOpen(
        $.IOServiceGetMatchingService(
            $.kIOMasterPortDefault,
            $.IOServiceMatching($.kIOHIDSystemClass)
        ),
        $.mach_task_self_,
        $.kIOHIDParamConnectType,
        ioConnect
    );
    $.IOHIDSetModifierLockState(ioConnect, $.kIOHIDCapsLockState, 0);
    $.IOServiceClose(ioConnect);
})();
