# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

xcb = """
typedef struct xcb_connection_t xcb_connection_t;  /**< Opaque structure containing all data that  XCB needs to communicate with an X server. */

typedef struct {
    void *data;   /**< Data of the current iterator */
    int rem;    /**< remaining elements */
    int index;  /**< index of the current iterator */
} xcb_generic_iterator_t;

typedef struct {
    uint8_t   response_type;  /**< Type of the response */
    uint8_t  pad0;           /**< Padding */
    uint16_t sequence;       /**< Sequence number */
    uint32_t length;         /**< Length of the response */
} xcb_generic_reply_t;

typedef struct {
    uint8_t   response_type;  /**< Type of the response */
    uint8_t  pad0;           /**< Padding */
    uint16_t sequence;       /**< Sequence number */
    uint32_t pad[7];         /**< Padding */
    uint32_t full_sequence;  /**< full sequence */
} xcb_generic_event_t;

typedef struct {
    uint8_t   response_type;  /**< Type of the response */
    uint8_t   error_code;     /**< Error code */
    uint16_t sequence;       /**< Sequence number */
    uint32_t resource_id;     /** < Resource ID for requests with side effects only */
    uint16_t minor_code;      /** < Minor opcode of the failed request */
    uint8_t major_code;       /** < Major opcode of the failed request */
    uint8_t pad0;
    uint32_t pad[5];         /**< Padding */
    uint32_t full_sequence;  /**< full sequence */
} xcb_generic_error_t;

typedef struct {
    unsigned int sequence;  /**< Sequence number */
} xcb_void_cookie_t;

typedef uint32_t xcb_window_t;
typedef uint32_t xcb_pixmap_t;
typedef uint32_t xcb_gcontext_t;
typedef uint32_t xcb_colormap_t;
typedef uint32_t xcb_drawable_t;
typedef uint32_t xcb_visualid_t;
typedef uint8_t xcb_keycode_t;
typedef uint32_t xcb_keysym_t;

typedef struct xcb_visualtype_t {
    xcb_visualid_t visual_id; /**<  */
    uint8_t        _class; /**<  */
    uint8_t        bits_per_rgb_value; /**<  */
    uint16_t       colormap_entries; /**<  */
    uint32_t       red_mask; /**<  */
    uint32_t       green_mask; /**<  */
    uint32_t       blue_mask; /**<  */
    uint8_t        pad0[4]; /**<  */
} xcb_visualtype_t;

typedef uint32_t xcb_timestamp_t;
typedef uint8_t xcb_button_t;
typedef uint32_t xcb_atom_t;

typedef enum xcb_config_window_t {
    XCB_CONFIG_WINDOW_X = 1,
    XCB_CONFIG_WINDOW_Y = 2,
    XCB_CONFIG_WINDOW_WIDTH = 4,
    XCB_CONFIG_WINDOW_HEIGHT = 8,
    XCB_CONFIG_WINDOW_BORDER_WIDTH = 16,
    XCB_CONFIG_WINDOW_SIBLING = 32,
    XCB_CONFIG_WINDOW_STACK_MODE = 64
} xcb_config_window_t;

typedef enum xcb_input_focus_t {
    XCB_INPUT_FOCUS_NONE = 0,
    XCB_INPUT_FOCUS_POINTER_ROOT = 1,
    XCB_INPUT_FOCUS_PARENT = 2,
    XCB_INPUT_FOCUS_FOLLOW_KEYBOARD = 3
} xcb_input_focus_t;

typedef enum xcb_time_t {
    XCB_TIME_CURRENT_TIME = 0
} xcb_time_t;

typedef enum xcb_atom_enum_t {
    XCB_ATOM_NONE = 0,
    XCB_ATOM_ANY = 0,
    XCB_ATOM_PRIMARY,
    XCB_ATOM_SECONDARY,
    XCB_ATOM_ARC,
    XCB_ATOM_ATOM,
    XCB_ATOM_BITMAP,
    XCB_ATOM_CARDINAL,
    XCB_ATOM_COLORMAP,
    XCB_ATOM_CURSOR,
    XCB_ATOM_CUT_BUFFER0,
    XCB_ATOM_CUT_BUFFER1,
    XCB_ATOM_CUT_BUFFER2,
    XCB_ATOM_CUT_BUFFER3,
    XCB_ATOM_CUT_BUFFER4,
    XCB_ATOM_CUT_BUFFER5,
    XCB_ATOM_CUT_BUFFER6,
    XCB_ATOM_CUT_BUFFER7,
    XCB_ATOM_DRAWABLE,
    XCB_ATOM_FONT,
    XCB_ATOM_INTEGER,
    XCB_ATOM_PIXMAP,
    XCB_ATOM_POINT,
    XCB_ATOM_RECTANGLE,
    XCB_ATOM_RESOURCE_MANAGER,
    XCB_ATOM_RGB_COLOR_MAP,
    XCB_ATOM_RGB_BEST_MAP,
    XCB_ATOM_RGB_BLUE_MAP,
    XCB_ATOM_RGB_DEFAULT_MAP,
    XCB_ATOM_RGB_GRAY_MAP,
    XCB_ATOM_RGB_GREEN_MAP,
    XCB_ATOM_RGB_RED_MAP,
    XCB_ATOM_STRING,
    XCB_ATOM_VISUALID,
    XCB_ATOM_WINDOW,
    XCB_ATOM_WM_COMMAND,
    XCB_ATOM_WM_HINTS,
    XCB_ATOM_WM_CLIENT_MACHINE,
    XCB_ATOM_WM_ICON_NAME,
    XCB_ATOM_WM_ICON_SIZE,
    XCB_ATOM_WM_NAME,
    XCB_ATOM_WM_NORMAL_HINTS,
    XCB_ATOM_WM_SIZE_HINTS,
    XCB_ATOM_WM_ZOOM_HINTS,
    XCB_ATOM_MIN_SPACE,
    XCB_ATOM_NORM_SPACE,
    XCB_ATOM_MAX_SPACE,
    XCB_ATOM_END_SPACE,
    XCB_ATOM_SUPERSCRIPT_X,
    XCB_ATOM_SUPERSCRIPT_Y,
    XCB_ATOM_SUBSCRIPT_X,
    XCB_ATOM_SUBSCRIPT_Y,
    XCB_ATOM_UNDERLINE_POSITION,
    XCB_ATOM_UNDERLINE_THICKNESS,
    XCB_ATOM_STRIKEOUT_ASCENT,
    XCB_ATOM_STRIKEOUT_DESCENT,
    XCB_ATOM_ITALIC_ANGLE,
    XCB_ATOM_X_HEIGHT,
    XCB_ATOM_QUAD_WIDTH,
    XCB_ATOM_WEIGHT,
    XCB_ATOM_POINT_SIZE,
    XCB_ATOM_RESOLUTION,
    XCB_ATOM_COPYRIGHT,
    XCB_ATOM_NOTICE,
    XCB_ATOM_FONT_NAME,
    XCB_ATOM_FAMILY_NAME,
    XCB_ATOM_FULL_NAME,
    XCB_ATOM_CAP_HEIGHT,
    XCB_ATOM_WM_CLASS,
    XCB_ATOM_WM_TRANSIENT_FOR
} xcb_atom_enum_t;

typedef enum xcb_get_property_type_t {
    XCB_GET_PROPERTY_TYPE_ANY = 0
} xcb_get_property_type_t;

typedef enum xcb_event_mask_t {
    XCB_EVENT_MASK_NO_EVENT = 0,
    XCB_EVENT_MASK_KEY_PRESS = 1,
    XCB_EVENT_MASK_KEY_RELEASE = 2,
    XCB_EVENT_MASK_BUTTON_PRESS = 4,
    XCB_EVENT_MASK_BUTTON_RELEASE = 8,
    XCB_EVENT_MASK_ENTER_WINDOW = 16,
    XCB_EVENT_MASK_LEAVE_WINDOW = 32,
    XCB_EVENT_MASK_POINTER_MOTION = 64,
    XCB_EVENT_MASK_POINTER_MOTION_HINT = 128,
    XCB_EVENT_MASK_BUTTON_1_MOTION = 256,
    XCB_EVENT_MASK_BUTTON_2_MOTION = 512,
    XCB_EVENT_MASK_BUTTON_3_MOTION = 1024,
    XCB_EVENT_MASK_BUTTON_4_MOTION = 2048,
    XCB_EVENT_MASK_BUTTON_5_MOTION = 4096,
    XCB_EVENT_MASK_BUTTON_MOTION = 8192,
    XCB_EVENT_MASK_KEYMAP_STATE = 16384,
    XCB_EVENT_MASK_EXPOSURE = 32768,
    XCB_EVENT_MASK_VISIBILITY_CHANGE = 65536,
    XCB_EVENT_MASK_STRUCTURE_NOTIFY = 131072,
    XCB_EVENT_MASK_RESIZE_REDIRECT = 262144,
    XCB_EVENT_MASK_SUBSTRUCTURE_NOTIFY = 524288,
    XCB_EVENT_MASK_SUBSTRUCTURE_REDIRECT = 1048576,
    XCB_EVENT_MASK_FOCUS_CHANGE = 2097152,
    XCB_EVENT_MASK_PROPERTY_CHANGE = 4194304,
    XCB_EVENT_MASK_COLOR_MAP_CHANGE = 8388608,
    XCB_EVENT_MASK_OWNER_GRAB_BUTTON = 16777216
} xcb_event_mask_t;

typedef enum xcb_mod_mask_t {
    XCB_MOD_MASK_SHIFT = 1,
    XCB_MOD_MASK_LOCK = 2,
    XCB_MOD_MASK_CONTROL = 4,
    XCB_MOD_MASK_1 = 8,
    XCB_MOD_MASK_2 = 16,
    XCB_MOD_MASK_3 = 32,
    XCB_MOD_MASK_4 = 64,
    XCB_MOD_MASK_5 = 128,
    XCB_MOD_MASK_ANY = 32768
} xcb_mod_mask_t;

typedef enum xcb_key_but_mask_t {
    XCB_KEY_BUT_MASK_SHIFT = 1,
    XCB_KEY_BUT_MASK_LOCK = 2,
    XCB_KEY_BUT_MASK_CONTROL = 4,
    XCB_KEY_BUT_MASK_MOD_1 = 8,
    XCB_KEY_BUT_MASK_MOD_2 = 16,
    XCB_KEY_BUT_MASK_MOD_3 = 32,
    XCB_KEY_BUT_MASK_MOD_4 = 64,
    XCB_KEY_BUT_MASK_MOD_5 = 128,
    XCB_KEY_BUT_MASK_BUTTON_1 = 256,
    XCB_KEY_BUT_MASK_BUTTON_2 = 512,
    XCB_KEY_BUT_MASK_BUTTON_3 = 1024,
    XCB_KEY_BUT_MASK_BUTTON_4 = 2048,
    XCB_KEY_BUT_MASK_BUTTON_5 = 4096
} xcb_key_but_mask_t;

typedef enum xcb_grab_mode_t {
    XCB_GRAB_MODE_SYNC = 0,
/**< The state of the keyboard appears to freeze: No further keyboard events are
generated by the server until the grabbing client issues a releasing
`AllowEvents` request or until the keyboard grab is released. */

    XCB_GRAB_MODE_ASYNC = 1
/**< Keyboard event processing continues normally. */

} xcb_grab_mode_t;


/** Opcode for xcb_key_press. */
#define XCB_KEY_PRESS ...

/**
 * @brief xcb_key_press_event_t
 **/
typedef struct xcb_key_press_event_t {
    uint8_t         response_type; /**<  */
    xcb_keycode_t   detail; /**<  */
    uint16_t        sequence; /**<  */
    xcb_timestamp_t time; /**<  */
    xcb_window_t    root; /**<  */
    xcb_window_t    event; /**<  */
    xcb_window_t    child; /**<  */
    int16_t         root_x; /**<  */
    int16_t         root_y; /**<  */
    int16_t         event_x; /**<  */
    int16_t         event_y; /**<  */
    uint16_t        state; /**<  */
    uint8_t         same_screen; /**<  */
    uint8_t         pad0; /**<  */
} xcb_key_press_event_t;

/** Opcode for xcb_key_release. */
#define XCB_KEY_RELEASE ...

typedef xcb_key_press_event_t xcb_key_release_event_t;

typedef enum xcb_button_mask_t {
    XCB_BUTTON_MASK_1 = 256,
    XCB_BUTTON_MASK_2 = 512,
    XCB_BUTTON_MASK_3 = 1024,
    XCB_BUTTON_MASK_4 = 2048,
    XCB_BUTTON_MASK_5 = 4096,
    XCB_BUTTON_MASK_ANY = 32768
} xcb_button_mask_t;

/** Opcode for xcb_button_press. */
#define XCB_BUTTON_PRESS ...

/**
 * @brief xcb_button_press_event_t
 **/
typedef struct xcb_button_press_event_t {
    uint8_t         response_type; /**<  */
    xcb_button_t    detail; /**<  */
    uint16_t        sequence; /**<  */
    xcb_timestamp_t time; /**<  */
    xcb_window_t    root; /**<  */
    xcb_window_t    event; /**<  */
    xcb_window_t    child; /**<  */
    int16_t         root_x; /**<  */
    int16_t         root_y; /**<  */
    int16_t         event_x; /**<  */
    int16_t         event_y; /**<  */
    uint16_t        state; /**<  */
    uint8_t         same_screen; /**<  */
    uint8_t         pad0; /**<  */
} xcb_button_press_event_t;

/** Opcode for xcb_button_release. */
#define XCB_BUTTON_RELEASE ...

typedef xcb_button_press_event_t xcb_button_release_event_t;

typedef enum xcb_motion_t {
    XCB_MOTION_NORMAL = 0,
    XCB_MOTION_HINT = 1
} xcb_motion_t;

/** Opcode for xcb_motion_notify. */
#define XCB_MOTION_NOTIFY ...

/**
 * @brief xcb_motion_notify_event_t
 **/
typedef struct xcb_motion_notify_event_t {
    uint8_t         response_type; /**<  */
    uint8_t         detail; /**<  */
    uint16_t        sequence; /**<  */
    xcb_timestamp_t time; /**<  */
    xcb_window_t    root; /**<  */
    xcb_window_t    event; /**<  */
    xcb_window_t    child; /**<  */
    int16_t         root_x; /**<  */
    int16_t         root_y; /**<  */
    int16_t         event_x; /**<  */
    int16_t         event_y; /**<  */
    uint16_t        state; /**<  */
    uint8_t         same_screen; /**<  */
    uint8_t         pad0; /**<  */
} xcb_motion_notify_event_t;

typedef enum xcb_notify_detail_t {
    XCB_NOTIFY_DETAIL_ANCESTOR = 0,
    XCB_NOTIFY_DETAIL_VIRTUAL = 1,
    XCB_NOTIFY_DETAIL_INFERIOR = 2,
    XCB_NOTIFY_DETAIL_NONLINEAR = 3,
    XCB_NOTIFY_DETAIL_NONLINEAR_VIRTUAL = 4,
    XCB_NOTIFY_DETAIL_POINTER = 5,
    XCB_NOTIFY_DETAIL_POINTER_ROOT = 6,
    XCB_NOTIFY_DETAIL_NONE = 7
} xcb_notify_detail_t;

typedef enum xcb_notify_mode_t {
    XCB_NOTIFY_MODE_NORMAL = 0,
    XCB_NOTIFY_MODE_GRAB = 1,
    XCB_NOTIFY_MODE_UNGRAB = 2,
    XCB_NOTIFY_MODE_WHILE_GRABBED = 3
} xcb_notify_mode_t;

/** Opcode for xcb_enter_notify. */
#define XCB_ENTER_NOTIFY ...

/**
 * @brief xcb_enter_notify_event_t
 **/
typedef struct xcb_enter_notify_event_t {
    uint8_t         response_type; /**<  */
    uint8_t         detail; /**<  */
    uint16_t        sequence; /**<  */
    xcb_timestamp_t time; /**<  */
    xcb_window_t    root; /**<  */
    xcb_window_t    event; /**<  */
    xcb_window_t    child; /**<  */
    int16_t         root_x; /**<  */
    int16_t         root_y; /**<  */
    int16_t         event_x; /**<  */
    int16_t         event_y; /**<  */
    uint16_t        state; /**<  */
    uint8_t         mode; /**<  */
    uint8_t         same_screen_focus; /**<  */
} xcb_enter_notify_event_t;

/** Opcode for xcb_leave_notify. */
#define XCB_LEAVE_NOTIFY ...

typedef xcb_enter_notify_event_t xcb_leave_notify_event_t;

/** Opcode for xcb_focus_in. */
#define XCB_FOCUS_IN ...

/**
 * @brief xcb_focus_in_event_t
 **/
typedef struct xcb_focus_in_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      detail; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t event; /**<  */
    uint8_t      mode; /**<  */
    uint8_t      pad0[3]; /**<  */
} xcb_focus_in_event_t;

/** Opcode for xcb_focus_out. */
#define XCB_FOCUS_OUT ...

typedef xcb_focus_in_event_t xcb_focus_out_event_t;

/** Opcode for xcb_keymap_notify. */
#define XCB_KEYMAP_NOTIFY ...

/**
 * @brief xcb_keymap_notify_event_t
 **/
typedef struct xcb_keymap_notify_event_t {
    uint8_t response_type; /**<  */
    uint8_t keys[31]; /**<  */
} xcb_keymap_notify_event_t;

/** Opcode for xcb_expose. */
#define XCB_EXPOSE ...

/**
 * @brief xcb_expose_event_t
 **/
typedef struct xcb_expose_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t window; /**<  */
    uint16_t     x; /**<  */
    uint16_t     y; /**<  */
    uint16_t     width; /**<  */
    uint16_t     height; /**<  */
    uint16_t     count; /**<  */
    uint8_t      pad1[2]; /**<  */
} xcb_expose_event_t;

/** Opcode for xcb_graphics_exposure. */
#define XCB_GRAPHICS_EXPOSURE ...

/**
 * @brief xcb_graphics_exposure_event_t
 **/
typedef struct xcb_graphics_exposure_event_t {
    uint8_t        response_type; /**<  */
    uint8_t        pad0; /**<  */
    uint16_t       sequence; /**<  */
    xcb_drawable_t drawable; /**<  */
    uint16_t       x; /**<  */
    uint16_t       y; /**<  */
    uint16_t       width; /**<  */
    uint16_t       height; /**<  */
    uint16_t       minor_opcode; /**<  */
    uint16_t       count; /**<  */
    uint8_t        major_opcode; /**<  */
    uint8_t        pad1[3]; /**<  */
} xcb_graphics_exposure_event_t;

/** Opcode for xcb_no_exposure. */
#define XCB_NO_EXPOSURE ...

/**
 * @brief xcb_no_exposure_event_t
 **/
typedef struct xcb_no_exposure_event_t {
    uint8_t        response_type; /**<  */
    uint8_t        pad0; /**<  */
    uint16_t       sequence; /**<  */
    xcb_drawable_t drawable; /**<  */
    uint16_t       minor_opcode; /**<  */
    uint8_t        major_opcode; /**<  */
    uint8_t        pad1; /**<  */
} xcb_no_exposure_event_t;

typedef enum xcb_visibility_t {
    XCB_VISIBILITY_UNOBSCURED = 0,
    XCB_VISIBILITY_PARTIALLY_OBSCURED = 1,
    XCB_VISIBILITY_FULLY_OBSCURED = 2
} xcb_visibility_t;

/** Opcode for xcb_visibility_notify. */
#define XCB_VISIBILITY_NOTIFY ...

/**
 * @brief xcb_visibility_notify_event_t
 **/
typedef struct xcb_visibility_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t window; /**<  */
    uint8_t      state; /**<  */
    uint8_t      pad1[3]; /**<  */
} xcb_visibility_notify_event_t;

/** Opcode for xcb_create_notify. */
#define XCB_CREATE_NOTIFY ...

/**
 * @brief xcb_create_notify_event_t
 **/
typedef struct xcb_create_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t parent; /**<  */
    xcb_window_t window; /**<  */
    int16_t      x; /**<  */
    int16_t      y; /**<  */
    uint16_t     width; /**<  */
    uint16_t     height; /**<  */
    uint16_t     border_width; /**<  */
    uint8_t      override_redirect; /**<  */
    uint8_t      pad1; /**<  */
} xcb_create_notify_event_t;

/** Opcode for xcb_destroy_notify. */
#define XCB_DESTROY_NOTIFY ...

/**
 * @brief xcb_destroy_notify_event_t
 **/
typedef struct xcb_destroy_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t event; /**<  */
    xcb_window_t window; /**<  */
} xcb_destroy_notify_event_t;

/** Opcode for xcb_unmap_notify. */
#define XCB_UNMAP_NOTIFY ...

/**
 * @brief xcb_unmap_notify_event_t
 **/
typedef struct xcb_unmap_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t event; /**<  */
    xcb_window_t window; /**<  */
    uint8_t      from_configure; /**<  */
    uint8_t      pad1[3]; /**<  */
} xcb_unmap_notify_event_t;

/** Opcode for xcb_map_notify. */
#define XCB_MAP_NOTIFY ...

/**
 * @brief xcb_map_notify_event_t
 **/
typedef struct xcb_map_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t event; /**<  */
    xcb_window_t window; /**<  */
    uint8_t      override_redirect; /**<  */
    uint8_t      pad1[3]; /**<  */
} xcb_map_notify_event_t;

/** Opcode for xcb_map_request. */
#define XCB_MAP_REQUEST ...

/**
 * @brief xcb_map_request_event_t
 **/
typedef struct xcb_map_request_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t parent; /**<  */
    xcb_window_t window; /**<  */
} xcb_map_request_event_t;

/** Opcode for xcb_reparent_notify. */
#define XCB_REPARENT_NOTIFY ...

/**
 * @brief xcb_reparent_notify_event_t
 **/
typedef struct xcb_reparent_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t event; /**<  */
    xcb_window_t window; /**<  */
    xcb_window_t parent; /**<  */
    int16_t      x; /**<  */
    int16_t      y; /**<  */
    uint8_t      override_redirect; /**<  */
    uint8_t      pad1[3]; /**<  */
} xcb_reparent_notify_event_t;

/** Opcode for xcb_configure_notify. */
#define XCB_CONFIGURE_NOTIFY ...

/**
 * @brief xcb_configure_notify_event_t
 **/
typedef struct xcb_configure_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t event; /**<  */
    xcb_window_t window; /**<  */
    xcb_window_t above_sibling; /**<  */
    int16_t      x; /**<  */
    int16_t      y; /**<  */
    uint16_t     width; /**<  */
    uint16_t     height; /**<  */
    uint16_t     border_width; /**<  */
    uint8_t      override_redirect; /**<  */
    uint8_t      pad1; /**<  */
} xcb_configure_notify_event_t;

/** Opcode for xcb_configure_request. */
#define XCB_CONFIGURE_REQUEST ...

/**
 * @brief xcb_configure_request_event_t
 **/
typedef struct xcb_configure_request_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      stack_mode; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t parent; /**<  */
    xcb_window_t window; /**<  */
    xcb_window_t sibling; /**<  */
    int16_t      x; /**<  */
    int16_t      y; /**<  */
    uint16_t     width; /**<  */
    uint16_t     height; /**<  */
    uint16_t     border_width; /**<  */
    uint16_t     value_mask; /**<  */
} xcb_configure_request_event_t;

/** Opcode for xcb_gravity_notify. */
#define XCB_GRAVITY_NOTIFY ...

/**
 * @brief xcb_gravity_notify_event_t
 **/
typedef struct xcb_gravity_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t event; /**<  */
    xcb_window_t window; /**<  */
    int16_t      x; /**<  */
    int16_t      y; /**<  */
} xcb_gravity_notify_event_t;

/** Opcode for xcb_resize_request. */
#define XCB_RESIZE_REQUEST ...

/**
 * @brief xcb_resize_request_event_t
 **/
typedef struct xcb_resize_request_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t window; /**<  */
    uint16_t     width; /**<  */
    uint16_t     height; /**<  */
} xcb_resize_request_event_t;

typedef enum xcb_place_t {
    XCB_PLACE_ON_TOP = 0,
/**< The window is now on top of all siblings. */

    XCB_PLACE_ON_BOTTOM = 1
/**< The window is now below all siblings. */

} xcb_place_t;

/** Opcode for xcb_circulate_notify. */
#define XCB_CIRCULATE_NOTIFY ...

/**
 * @brief xcb_circulate_notify_event_t
 **/
typedef struct xcb_circulate_notify_event_t {
    uint8_t      response_type; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     sequence; /**<  */
    xcb_window_t event; /**<  */
    xcb_window_t window; /**<  */
    uint8_t      pad1[4]; /**<  */
    uint8_t      place; /**<  */
    uint8_t      pad2[3]; /**<  */
} xcb_circulate_notify_event_t;

/** Opcode for xcb_circulate_request. */
#define XCB_CIRCULATE_REQUEST ...

typedef xcb_circulate_notify_event_t xcb_circulate_request_event_t;

typedef enum xcb_property_t {
    XCB_PROPERTY_NEW_VALUE = 0,
    XCB_PROPERTY_DELETE = 1
} xcb_property_t;

/** Opcode for xcb_property_notify. */
#define XCB_PROPERTY_NOTIFY ...

/**
 * @brief xcb_property_notify_event_t
 **/
typedef struct xcb_property_notify_event_t {
    uint8_t         response_type; /**<  */
    uint8_t         pad0; /**<  */
    uint16_t        sequence; /**<  */
    xcb_window_t    window; /**<  */
    xcb_atom_t      atom; /**<  */
    xcb_timestamp_t time; /**<  */
    uint8_t         state; /**<  */
    uint8_t         pad1[3]; /**<  */
} xcb_property_notify_event_t;

/** Opcode for xcb_selection_clear. */
#define XCB_SELECTION_CLEAR ...

/**
 * @brief xcb_selection_clear_event_t
 **/
typedef struct xcb_selection_clear_event_t {
    uint8_t         response_type; /**<  */
    uint8_t         pad0; /**<  */
    uint16_t        sequence; /**<  */
    xcb_timestamp_t time; /**<  */
    xcb_window_t    owner; /**<  */
    xcb_atom_t      selection; /**<  */
} xcb_selection_clear_event_t;

/** Opcode for xcb_selection_request. */
#define XCB_SELECTION_REQUEST ...

/**
 * @brief xcb_selection_request_event_t
 **/
typedef struct xcb_selection_request_event_t {
    uint8_t         response_type; /**<  */
    uint8_t         pad0; /**<  */
    uint16_t        sequence; /**<  */
    xcb_timestamp_t time; /**<  */
    xcb_window_t    owner; /**<  */
    xcb_window_t    requestor; /**<  */
    xcb_atom_t      selection; /**<  */
    xcb_atom_t      target; /**<  */
    xcb_atom_t      property; /**<  */
} xcb_selection_request_event_t;

/** Opcode for xcb_selection_notify. */
#define XCB_SELECTION_NOTIFY ...

/**
 * @brief xcb_selection_notify_event_t
 **/
typedef struct xcb_selection_notify_event_t {
    uint8_t         response_type; /**<  */
    uint8_t         pad0; /**<  */
    uint16_t        sequence; /**<  */
    xcb_timestamp_t time; /**<  */
    xcb_window_t    requestor; /**<  */
    xcb_atom_t      selection; /**<  */
    xcb_atom_t      target; /**<  */
    xcb_atom_t      property; /**<  */
} xcb_selection_notify_event_t;

typedef enum xcb_colormap_state_t {
    XCB_COLORMAP_STATE_UNINSTALLED = 0,
/**< The colormap was uninstalled. */

    XCB_COLORMAP_STATE_INSTALLED = 1
/**< The colormap was installed. */

} xcb_colormap_state_t;

typedef enum xcb_colormap_enum_t {
    XCB_COLORMAP_NONE = 0
} xcb_colormap_enum_t;

/** Opcode for xcb_colormap_notify. */
#define XCB_COLORMAP_NOTIFY ...

/**
 * @brief xcb_colormap_notify_event_t
 **/
typedef struct xcb_colormap_notify_event_t {
    uint8_t        response_type; /**<  */
    uint8_t        pad0; /**<  */
    uint16_t       sequence; /**<  */
    xcb_window_t   window; /**<  */
    xcb_colormap_t colormap; /**<  */
    uint8_t        _new; /**<  */
    uint8_t        state; /**<  */
    uint8_t        pad1[2]; /**<  */
} xcb_colormap_notify_event_t;

/**
 * @brief xcb_client_message_data_t
 **/
typedef union xcb_client_message_data_t {
    uint8_t  data8[20]; /**<  */
    uint16_t data16[10]; /**<  */
    uint32_t data32[5]; /**<  */
} xcb_client_message_data_t;

/**
 * @brief xcb_client_message_data_iterator_t
 **/
typedef struct xcb_client_message_data_iterator_t {
    xcb_client_message_data_t *data; /**<  */
    int                        rem; /**<  */
    int                        index; /**<  */
} xcb_client_message_data_iterator_t;

/** Opcode for xcb_client_message. */
#define XCB_CLIENT_MESSAGE ...

/**
 * @brief xcb_client_message_event_t
 **/
typedef struct xcb_client_message_event_t {
    uint8_t                   response_type; /**<  */
    uint8_t                   format; /**<  */
    uint16_t                  sequence; /**<  */
    xcb_window_t              window; /**<  */
    xcb_atom_t                type; /**<  */
    xcb_client_message_data_t data; /**<  */
} xcb_client_message_event_t;

typedef enum xcb_mapping_t {
    XCB_MAPPING_MODIFIER = 0,
    XCB_MAPPING_KEYBOARD = 1,
    XCB_MAPPING_POINTER = 2
} xcb_mapping_t;

/** Opcode for xcb_mapping_notify. */
#define XCB_MAPPING_NOTIFY ...

/**
 * @brief xcb_mapping_notify_event_t
 **/
typedef struct xcb_mapping_notify_event_t {
    uint8_t       response_type; /**<  */
    uint8_t       pad0; /**<  */
    uint16_t      sequence; /**<  */
    uint8_t       request; /**<  */
    xcb_keycode_t first_keycode; /**<  */
    uint8_t       count; /**<  */
    uint8_t       pad1; /**<  */
} xcb_mapping_notify_event_t;

/**
 * @brief xcb_alloc_color_cookie_t
 **/
typedef struct xcb_alloc_color_cookie_t {
    unsigned int sequence; /**<  */
} xcb_alloc_color_cookie_t;

/** Opcode for xcb_alloc_color. */
#define XCB_ALLOC_COLOR ...

/**
 * @brief xcb_alloc_color_request_t
 **/
typedef struct xcb_alloc_color_request_t {
    uint8_t        major_opcode; /**<  */
    uint8_t        pad0; /**<  */
    uint16_t       length; /**<  */
    xcb_colormap_t cmap; /**<  */
    uint16_t       red; /**<  */
    uint16_t       green; /**<  */
    uint16_t       blue; /**<  */
    uint8_t        pad1[2]; /**<  */
} xcb_alloc_color_request_t;

/**
 * @brief xcb_alloc_color_reply_t
 **/
typedef struct xcb_alloc_color_reply_t {
    uint8_t  response_type; /**<  */
    uint8_t  pad0; /**<  */
    uint16_t sequence; /**<  */
    uint32_t length; /**<  */
    uint16_t red; /**<  */
    uint16_t green; /**<  */
    uint16_t blue; /**<  */
    uint8_t  pad1[2]; /**<  */
    uint32_t pixel; /**<  */
} xcb_alloc_color_reply_t;

/**
 * @brief xcb_alloc_named_color_cookie_t
 **/
typedef struct xcb_alloc_named_color_cookie_t {
    unsigned int sequence; /**<  */
} xcb_alloc_named_color_cookie_t;

/** Opcode for xcb_alloc_named_color. */
#define XCB_ALLOC_NAMED_COLOR ...

/**
 * @brief xcb_alloc_named_color_request_t
 **/
typedef struct xcb_alloc_named_color_request_t {
    uint8_t        major_opcode; /**<  */
    uint8_t        pad0; /**<  */
    uint16_t       length; /**<  */
    xcb_colormap_t cmap; /**<  */
    uint16_t       name_len; /**<  */
    uint8_t        pad1[2]; /**<  */
} xcb_alloc_named_color_request_t;

/**
 * @brief xcb_alloc_named_color_reply_t
 **/
typedef struct xcb_alloc_named_color_reply_t {
    uint8_t  response_type; /**<  */
    uint8_t  pad0; /**<  */
    uint16_t sequence; /**<  */
    uint32_t length; /**<  */
    uint32_t pixel; /**<  */
    uint16_t exact_red; /**<  */
    uint16_t exact_green; /**<  */
    uint16_t exact_blue; /**<  */
    uint16_t visual_red; /**<  */
    uint16_t visual_green; /**<  */
    uint16_t visual_blue; /**<  */
} xcb_alloc_named_color_reply_t;

/**
 * @brief xcb_get_property_cookie_t
 **/
typedef struct xcb_get_property_cookie_t {
    unsigned int sequence; /**<  */
} xcb_get_property_cookie_t;

/** Opcode for xcb_get_property. */
#define XCB_GET_PROPERTY ...

/**
 * @brief xcb_get_property_request_t
 **/
typedef struct xcb_get_property_request_t {
    uint8_t      major_opcode; /**<  */
    uint8_t      _delete; /**<  */
    uint16_t     length; /**<  */
    xcb_window_t window; /**<  */
    xcb_atom_t   property; /**<  */
    xcb_atom_t   type; /**<  */
    uint32_t     long_offset; /**<  */
    uint32_t     long_length; /**<  */
} xcb_get_property_request_t;

/**
 * @brief xcb_get_property_reply_t
 **/
typedef struct xcb_get_property_reply_t {
    uint8_t    response_type; /**<  */
    uint8_t    format; /**<  */
    uint16_t   sequence; /**<  */
    uint32_t   length; /**<  */
    xcb_atom_t type; /**<  */
    uint32_t   bytes_after; /**<  */
    uint32_t   value_len; /**<  */
    uint8_t    pad0[12]; /**<  */
} xcb_get_property_reply_t;

/**
 * @brief xcb_list_properties_cookie_t
 **/
typedef struct xcb_list_properties_cookie_t {
    unsigned int sequence; /**<  */
} xcb_list_properties_cookie_t;

/** Opcode for xcb_list_properties. */
#define XCB_LIST_PROPERTIES ...

/**
 * @brief xcb_list_properties_request_t
 **/
typedef struct xcb_list_properties_request_t {
    uint8_t      major_opcode; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     length; /**<  */
    xcb_window_t window; /**<  */
} xcb_list_properties_request_t;

/**
 * @brief xcb_list_properties_reply_t
 **/
typedef struct xcb_list_properties_reply_t {
    uint8_t  response_type; /**<  */
    uint8_t  pad0; /**<  */
    uint16_t sequence; /**<  */
    uint32_t length; /**<  */
    uint16_t atoms_len; /**<  */
    uint8_t  pad1[22]; /**<  */
} xcb_list_properties_reply_t;

/**
 * @brief xcb_get_keyboard_mapping_cookie_t
 **/
typedef struct xcb_get_keyboard_mapping_cookie_t {
    unsigned int sequence; /**<  */
} xcb_get_keyboard_mapping_cookie_t;

/** Opcode for xcb_get_keyboard_mapping. */
#define XCB_GET_KEYBOARD_MAPPING ...

/**
 * @brief xcb_get_keyboard_mapping_request_t
 **/
typedef struct xcb_get_keyboard_mapping_request_t {
    uint8_t       major_opcode; /**<  */
    uint8_t       pad0; /**<  */
    uint16_t      length; /**<  */
    xcb_keycode_t first_keycode; /**<  */
    uint8_t       count; /**<  */
} xcb_get_keyboard_mapping_request_t;

/**
 * @brief xcb_get_keyboard_mapping_reply_t
 **/
typedef struct xcb_get_keyboard_mapping_reply_t {
    uint8_t  response_type; /**<  */
    uint8_t  keysyms_per_keycode; /**<  */
    uint16_t sequence; /**<  */
    uint32_t length; /**<  */
    uint8_t  pad0[24]; /**<  */
} xcb_get_keyboard_mapping_reply_t;

/**
 * @brief xcb_get_modifier_mapping_cookie_t
 **/
typedef struct xcb_get_modifier_mapping_cookie_t {
    unsigned int sequence; /**<  */
} xcb_get_modifier_mapping_cookie_t;

/** Opcode for xcb_get_modifier_mapping. */
#define XCB_GET_MODIFIER_MAPPING ...

/**
 * @brief xcb_get_modifier_mapping_request_t
 **/
typedef struct xcb_get_modifier_mapping_request_t {
    uint8_t  major_opcode; /**<  */
    uint8_t  pad0; /**<  */
    uint16_t length; /**<  */
} xcb_get_modifier_mapping_request_t;

/**
 * @brief xcb_get_modifier_mapping_reply_t
 **/
typedef struct xcb_get_modifier_mapping_reply_t {
    uint8_t  response_type; /**<  */
    uint8_t  keycodes_per_modifier; /**<  */
    uint16_t sequence; /**<  */
    uint32_t length; /**<  */
    uint8_t  pad0[24]; /**<  */
} xcb_get_modifier_mapping_reply_t;

typedef enum xcb_grab_t {
    XCB_GRAB_ANY = 0
} xcb_grab_t;

/** Opcode for xcb_grab_key. */
#define XCB_GRAB_KEY ...

/**
 * @brief xcb_grab_key_request_t
 **/
typedef struct xcb_grab_key_request_t {
    uint8_t       major_opcode; /**<  */
    uint8_t       owner_events; /**<  */
    uint16_t      length; /**<  */
    xcb_window_t  grab_window; /**<  */
    uint16_t      modifiers; /**<  */
    xcb_keycode_t key; /**<  */
    uint8_t       pointer_mode; /**<  */
    uint8_t       keyboard_mode; /**<  */
    uint8_t       pad0[3]; /**<  */
} xcb_grab_key_request_t;

/** Opcode for xcb_ungrab_key. */
#define XCB_UNGRAB_KEY ...

/**
 * @brief xcb_ungrab_key_request_t
 **/
typedef struct xcb_ungrab_key_request_t {
    uint8_t       major_opcode; /**<  */
    xcb_keycode_t key; /**<  */
    uint16_t      length; /**<  */
    xcb_window_t  grab_window; /**<  */
    uint16_t      modifiers; /**<  */
    uint8_t       pad0[2]; /**<  */
} xcb_ungrab_key_request_t;


typedef enum xcb_map_state_t {
    XCB_MAP_STATE_UNMAPPED = 0,
    XCB_MAP_STATE_UNVIEWABLE = 1,
    XCB_MAP_STATE_VIEWABLE = 2
} xcb_map_state_t;

/**
 * @brief xcb_get_window_attributes_cookie_t
 **/
typedef struct xcb_get_window_attributes_cookie_t {
    unsigned int sequence; /**<  */
} xcb_get_window_attributes_cookie_t;


/**
 * @brief xcb_get_window_attributes_request_t
 **/
typedef struct xcb_get_window_attributes_request_t {
    uint8_t      major_opcode; /**<  */
    uint8_t      pad0; /**<  */
    uint16_t     length; /**<  */
    xcb_window_t window; /**<  */
} xcb_get_window_attributes_request_t;

/**
 * @brief xcb_get_window_attributes_reply_t
 **/
typedef struct xcb_get_window_attributes_reply_t {
    uint8_t        response_type; /**<  */
    uint8_t        backing_store; /**<  */
    uint16_t       sequence; /**<  */
    uint32_t       length; /**<  */
    xcb_visualid_t visual; /**<  */
    uint16_t       _class; /**<  */
    uint8_t        bit_gravity; /**<  */
    uint8_t        win_gravity; /**<  */
    uint32_t       backing_planes; /**<  */
    uint32_t       backing_pixel; /**<  */
    uint8_t        save_under; /**<  */
    uint8_t        map_is_installed; /**<  */
    uint8_t        map_state; /**<  */
    uint8_t        override_redirect; /**<  */
    xcb_colormap_t colormap; /**<  */
    uint32_t       all_event_masks; /**<  */
    uint32_t       your_event_mask; /**<  */
    uint16_t       do_not_propagate_mask; /**<  */
    uint8_t        pad0[2]; /**<  */
} xcb_get_window_attributes_reply_t;


/**
 * @brief xcb_get_geometry_cookie_t
 **/
typedef struct xcb_get_geometry_cookie_t {
    unsigned int sequence; /**<  */
} xcb_get_geometry_cookie_t;

/**
 * @brief xcb_get_geometry_reply_t
 **/
typedef struct xcb_get_geometry_reply_t {
    uint8_t      response_type; /**<  */
    uint8_t      depth; /**<  */
    uint16_t     sequence; /**<  */
    uint32_t     length; /**<  */
    xcb_window_t root; /**<  */
    int16_t      x; /**<  */
    int16_t      y; /**<  */
    uint16_t     width; /**<  */
    uint16_t     height; /**<  */
    uint16_t     border_width; /**<  */
    uint8_t      pad0[2]; /**<  */
} xcb_get_geometry_reply_t;

/**
 * @brief xcb_intern_atom_cookie_t
 **/
typedef struct xcb_intern_atom_cookie_t {
    unsigned int sequence; /**<  */
} xcb_intern_atom_cookie_t;

/** Opcode for xcb_intern_atom. */
#define XCB_INTERN_ATOM ...

/**
 * @brief xcb_intern_atom_request_t
 **/
typedef struct xcb_intern_atom_request_t {
    uint8_t  major_opcode; /**<  */
    uint8_t  only_if_exists; /**<  */
    uint16_t length; /**<  */
    uint16_t name_len; /**<  */
    uint8_t  pad0[2]; /**<  */
} xcb_intern_atom_request_t;

/**
 * @brief xcb_intern_atom_reply_t
 **/
typedef struct xcb_intern_atom_reply_t {
    uint8_t    response_type; /**<  */
    uint8_t    pad0; /**<  */
    uint16_t   sequence; /**<  */
    uint32_t   length; /**<  */
    xcb_atom_t atom; /**<  */
} xcb_intern_atom_reply_t;

/**
 * @brief xcb_get_atom_name_cookie_t
 **/
typedef struct xcb_get_atom_name_cookie_t {
    unsigned int sequence; /**<  */
} xcb_get_atom_name_cookie_t;

/** Opcode for xcb_get_atom_name. */
#define XCB_GET_ATOM_NAME ...

/**
 * @brief xcb_get_atom_name_request_t
 **/
typedef struct xcb_get_atom_name_request_t {
    uint8_t    major_opcode; /**<  */
    uint8_t    pad0; /**<  */
    uint16_t   length; /**<  */
    xcb_atom_t atom; /**<  */
} xcb_get_atom_name_request_t;

/**
 * @brief xcb_get_atom_name_reply_t
 **/
typedef struct xcb_get_atom_name_reply_t {
    uint8_t  response_type; /**<  */
    uint8_t  pad0; /**<  */
    uint16_t sequence; /**<  */
    uint32_t length; /**<  */
    uint16_t name_len; /**<  */
    uint8_t  pad1[22]; /**<  */
} xcb_get_atom_name_reply_t;


typedef struct xcb_screen_t {
    xcb_window_t   root; /**<  */
    xcb_colormap_t default_colormap; /**<  */
    uint32_t       white_pixel; /**<  */
    uint32_t       black_pixel; /**<  */
    uint32_t       current_input_masks; /**<  */
    uint16_t       width_in_pixels; /**<  */
    uint16_t       height_in_pixels; /**<  */
    uint16_t       width_in_millimeters; /**<  */
    uint16_t       height_in_millimeters; /**<  */
    uint16_t       min_installed_maps; /**<  */
    uint16_t       max_installed_maps; /**<  */
    xcb_visualid_t root_visual; /**<  */
    uint8_t        backing_stores; /**<  */
    uint8_t        save_unders; /**<  */
    uint8_t        root_depth; /**<  */
    uint8_t        allowed_depths_len; /**<  */
} xcb_screen_t;

typedef struct xcb_screen_iterator_t {
    xcb_screen_t *data; /**<  */
    int           rem; /**<  */
    int           index; /**<  */
} xcb_screen_iterator_t;

typedef struct xcb_setup_request_t {
    uint8_t  byte_order; /**<  */
    uint8_t  pad0; /**<  */
    uint16_t protocol_major_version; /**<  */
    uint16_t protocol_minor_version; /**<  */
    uint16_t authorization_protocol_name_len; /**<  */
    uint16_t authorization_protocol_data_len; /**<  */
    uint8_t  pad1[2]; /**<  */
} xcb_setup_request_t;

typedef struct xcb_setup_request_iterator_t {
    xcb_setup_request_t *data; /**<  */
    int                  rem; /**<  */
    int                  index; /**<  */
} xcb_setup_request_iterator_t;

typedef struct xcb_setup_t {
    uint8_t       status; /**<  */
    uint8_t       pad0; /**<  */
    uint16_t      protocol_major_version; /**<  */
    uint16_t      protocol_minor_version; /**<  */
    uint16_t      length; /**<  */
    uint32_t      release_number; /**<  */
    uint32_t      resource_id_base; /**<  */
    uint32_t      resource_id_mask; /**<  */
    uint32_t      motion_buffer_size; /**<  */
    uint16_t      vendor_len; /**<  */
    uint16_t      maximum_request_length; /**<  */
    uint8_t       roots_len; /**<  */
    uint8_t       pixmap_formats_len; /**<  */
    uint8_t       image_byte_order; /**<  */
    uint8_t       bitmap_format_bit_order; /**<  */
    uint8_t       bitmap_format_scanline_unit; /**<  */
    uint8_t       bitmap_format_scanline_pad; /**<  */
    xcb_keycode_t min_keycode; /**<  */
    xcb_keycode_t max_keycode; /**<  */
    uint8_t       pad1[4]; /**<  */
} xcb_setup_t;

typedef struct xcb_setup_iterator_t {
    xcb_setup_t *data; /**<  */
    int          rem; /**<  */
    int          index; /**<  */
} xcb_setup_iterator_t;

typedef enum xcb_window_class_t {
    XCB_WINDOW_CLASS_COPY_FROM_PARENT = 0,
    XCB_WINDOW_CLASS_INPUT_OUTPUT = 1,
    XCB_WINDOW_CLASS_INPUT_ONLY = 2
} xcb_window_class_t;


typedef enum xcb_cw_t {
    XCB_CW_BACK_PIXMAP = 1,
/**< Overrides the default background-pixmap. The background pixmap and window must
have the same root and same depth. Any size pixmap can be used, although some
sizes may be faster than others.

If `XCB_BACK_PIXMAP_NONE` is specified, the window has no defined background.
The server may fill the contents with the previous screen contents or with
contents of its own choosing.

If `XCB_BACK_PIXMAP_PARENT_RELATIVE` is specified, the parent's background is
used, but the window must have the same depth as the parent (or a Match error
results).   The parent's background is tracked, and the current version is
used each time the window background is required. */

    XCB_CW_BACK_PIXEL = 2,
/**< Overrides `BackPixmap`. A pixmap of undefined size filled with the specified
background pixel is used for the background. Range-checking is not performed,
the background pixel is truncated to the appropriate number of bits. */

    XCB_CW_BORDER_PIXMAP = 4,
/**< Overrides the default border-pixmap. The border pixmap and window must have the
same root and the same depth. Any size pixmap can be used, although some sizes
may be faster than others.

The special value `XCB_COPY_FROM_PARENT` means the parent's border pixmap is
copied (subsequent changes to the parent's border attribute do not affect the
child), but the window must have the same depth as the parent. */

    XCB_CW_BORDER_PIXEL = 8,
/**< Overrides `BorderPixmap`. A pixmap of undefined size filled with the specified
border pixel is used for the border. Range checking is not performed on the
border-pixel value, it is truncated to the appropriate number of bits. */

    XCB_CW_BIT_GRAVITY = 16,
/**< Defines which region of the window should be retained if the window is resized. */

    XCB_CW_WIN_GRAVITY = 32,
/**< Defines how the window should be repositioned if the parent is resized (see
`ConfigureWindow`). */

    XCB_CW_BACKING_STORE = 64,
/**< A backing-store of `WhenMapped` advises the server that maintaining contents of
obscured regions when the window is mapped would be beneficial. A backing-store
of `Always` advises the server that maintaining contents even when the window
is unmapped would be beneficial. In this case, the server may generate an
exposure event when the window is created. A value of `NotUseful` advises the
server that maintaining contents is unnecessary, although a server may still
choose to maintain contents while the window is mapped. Note that if the server
maintains contents, then the server should maintain complete contents not just
the region within the parent boundaries, even if the window is larger than its
parent. While the server maintains contents, exposure events will not normally
be generated, but the server may stop maintaining contents at any time. */

    XCB_CW_BACKING_PLANES = 128,
/**< The backing-planes indicates (with bits set to 1) which bit planes of the
window hold dynamic data that must be preserved in backing-stores and during
save-unders. */

    XCB_CW_BACKING_PIXEL = 256,
/**< The backing-pixel specifies what value to use in planes not covered by
backing-planes. The server is free to save only the specified bit planes in the
backing-store or save-under and regenerate the remaining planes with the
specified pixel value. Any bits beyond the specified depth of the window in
these values are simply ignored. */

    XCB_CW_OVERRIDE_REDIRECT = 512,
/**< The override-redirect specifies whether map and configure requests on this
window should override a SubstructureRedirect on the parent, typically to
inform a window manager not to tamper with the window. */

    XCB_CW_SAVE_UNDER = 1024,
/**< If 1, the server is advised that when this window is mapped, saving the
contents of windows it obscures would be beneficial. */

    XCB_CW_EVENT_MASK = 2048,
/**< The event-mask defines which events the client is interested in for this window
(or for some event types, inferiors of the window). */

    XCB_CW_DONT_PROPAGATE = 4096,
/**< The do-not-propagate-mask defines which events should not be propagated to
ancestor windows when no client has the event type selected in this window. */

    XCB_CW_COLORMAP = 8192,
/**< The colormap specifies the colormap that best reflects the true colors of the window. Servers
capable of supporting multiple hardware colormaps may use this information, and window man-
agers may use it for InstallColormap requests. The colormap must have the same visual type
and root as the window (or a Match error results). If CopyFromParent is specified, the parent's
colormap is copied (subsequent changes to the parent's colormap attribute do not affect the child).
However, the window must have the same visual type as the parent (or a Match error results),
and the parent must not have a colormap of None (or a Match error results). For an explanation
of None, see FreeColormap request. The colormap is copied by sharing the colormap object
between the child and the parent, not by making a complete copy of the colormap contents. */

    XCB_CW_CURSOR = 16384
/**< If a cursor is specified, it will be used whenever the pointer is in the window. If None is speci-
fied, the parent's cursor will be used when the pointer is in the window, and any change in the
parent's cursor will cause an immediate change in the displayed cursor. */

} xcb_cw_t;

typedef enum xcb_gc_t {
    XCB_GC_FUNCTION = 1,
/**< TODO: Refer to GX */

    XCB_GC_PLANE_MASK = 2,
/**< In graphics operations, given a source and destination pixel, the result is
computed bitwise on corresponding bits of the pixels; that is, a Boolean
operation is performed in each bit plane. The plane-mask restricts the
operation to a subset of planes, so the result is:

        ((src FUNC dst) AND plane-mask) OR (dst AND (NOT plane-mask)) */

    XCB_GC_FOREGROUND = 4,
/**< Foreground colorpixel. */

    XCB_GC_BACKGROUND = 8,
/**< Background colorpixel. */

    XCB_GC_LINE_WIDTH = 16,
/**< The line-width is measured in pixels and can be greater than or equal to one, a wide line, or the
special value zero, a thin line. */

    XCB_GC_LINE_STYLE = 32,
/**< The line-style defines which sections of a line are drawn:
Solid                The full path of the line is drawn.
DoubleDash           The full path of the line is drawn, but the even dashes are filled differently
                     than the odd dashes (see fill-style), with Butt cap-style used where even and
                     odd dashes meet.
OnOffDash            Only the even dashes are drawn, and cap-style applies to all internal ends of
                     the individual dashes (except NotLast is treated as Butt). */

    XCB_GC_CAP_STYLE = 64,
/**< The cap-style defines how the endpoints of a path are drawn:
NotLast    The result is equivalent to Butt, except that for a line-width of zero the final
           endpoint is not drawn.
Butt       The result is square at the endpoint (perpendicular to the slope of the line)
           with no projection beyond.
Round      The result is a circular arc with its diameter equal to the line-width, centered
           on the endpoint; it is equivalent to Butt for line-width zero.
Projecting The result is square at the end, but the path continues beyond the endpoint for
           a distance equal to half the line-width; it is equivalent to Butt for line-width
           zero. */

    XCB_GC_JOIN_STYLE = 128,
/**< The join-style defines how corners are drawn for wide lines:
Miter               The outer edges of the two lines extend to meet at an angle. However, if the
                    angle is less than 11 degrees, a Bevel join-style is used instead.
Round               The result is a circular arc with a diameter equal to the line-width, centered
                    on the joinpoint.
Bevel               The result is Butt endpoint styles, and then the triangular notch is filled. */

    XCB_GC_FILL_STYLE = 256,
/**< The fill-style defines the contents of the source for line, text, and fill requests. For all text and fill
requests (for example, PolyText8, PolyText16, PolyFillRectangle, FillPoly, and PolyFillArc)
as well as for line requests with line-style Solid, (for example, PolyLine, PolySegment,
PolyRectangle, PolyArc) and for the even dashes for line requests with line-style OnOffDash
or DoubleDash:
Solid                     Foreground
Tiled                     Tile
OpaqueStippled            A tile with the same width and height as stipple but with background
                          everywhere stipple has a zero and with foreground everywhere stipple
                          has a one
Stippled                  Foreground masked by stipple
For the odd dashes for line requests with line-style DoubleDash:
Solid                     Background
Tiled                     Same as for even dashes
OpaqueStippled            Same as for even dashes
Stippled                  Background masked by stipple */

    XCB_GC_FILL_RULE = 512,
/**<  */

    XCB_GC_TILE = 1024,
/**< The tile/stipple represents an infinite two-dimensional plane with the tile/stipple replicated in all
dimensions. When that plane is superimposed on the drawable for use in a graphics operation,
the upper-left corner of some instance of the tile/stipple is at the coordinates within the drawable
specified by the tile/stipple origin. The tile/stipple and clip origins are interpreted relative to the
origin of whatever destination drawable is specified in a graphics request.
The tile pixmap must have the same root and depth as the gcontext (or a Match error results).
The stipple pixmap must have depth one and must have the same root as the gcontext (or a
Match error results). For fill-style Stippled (but not fill-style
OpaqueStippled), the stipple pattern is tiled in a single plane and acts as an
additional clip mask to be ANDed with the clip-mask.
Any size pixmap can be used for tiling or stippling, although some sizes may be faster to use than
others. */

    XCB_GC_STIPPLE = 2048,
/**< The tile/stipple represents an infinite two-dimensional plane with the tile/stipple replicated in all
dimensions. When that plane is superimposed on the drawable for use in a graphics operation,
the upper-left corner of some instance of the tile/stipple is at the coordinates within the drawable
specified by the tile/stipple origin. The tile/stipple and clip origins are interpreted relative to the
origin of whatever destination drawable is specified in a graphics request.
The tile pixmap must have the same root and depth as the gcontext (or a Match error results).
The stipple pixmap must have depth one and must have the same root as the gcontext (or a
Match error results). For fill-style Stippled (but not fill-style
OpaqueStippled), the stipple pattern is tiled in a single plane and acts as an
additional clip mask to be ANDed with the clip-mask.
Any size pixmap can be used for tiling or stippling, although some sizes may be faster to use than
others. */

    XCB_GC_TILE_STIPPLE_ORIGIN_X = 4096,
/**< TODO */

    XCB_GC_TILE_STIPPLE_ORIGIN_Y = 8192,
/**< TODO */

    XCB_GC_FONT = 16384,
/**< Which font to use for the `ImageText8` and `ImageText16` requests. */

    XCB_GC_SUBWINDOW_MODE = 32768,
/**< For ClipByChildren, both source and destination windows are additionally
clipped by all viewable InputOutput children. For IncludeInferiors, neither
source nor destination window is
clipped by inferiors. This will result in including subwindow contents in the source and drawing
through subwindow boundaries of the destination. The use of IncludeInferiors with a source or
destination window of one depth with mapped inferiors of differing depth is not illegal, but the
semantics is undefined by the core protocol. */

    XCB_GC_GRAPHICS_EXPOSURES = 65536,
/**< Whether ExposureEvents should be generated (1) or not (0).

The default is 1. */

    XCB_GC_CLIP_ORIGIN_X = 131072,
/**< TODO */

    XCB_GC_CLIP_ORIGIN_Y = 262144,
/**< TODO */

    XCB_GC_CLIP_MASK = 524288,
/**< The clip-mask restricts writes to the destination drawable. Only pixels where the clip-mask has
bits set to 1 are drawn. Pixels are not drawn outside the area covered by the clip-mask or where
the clip-mask has bits set to 0. The clip-mask affects all graphics requests, but it does not clip
sources. The clip-mask origin is interpreted relative to the origin of whatever destination drawable is specified in a graphics request. If a pixmap is specified as the clip-mask, it must have
depth 1 and have the same root as the gcontext (or a Match error results). If clip-mask is None,
then pixels are always drawn, regardless of the clip origin. The clip-mask can also be set with the
SetClipRectangles request. */

    XCB_GC_DASH_OFFSET = 1048576,
/**< TODO */

    XCB_GC_DASH_LIST = 2097152,
/**< TODO */

    XCB_GC_ARC_MODE = 4194304
/**< TODO */

} xcb_gc_t;



int xcb_flush(xcb_connection_t *c);
xcb_generic_event_t *xcb_poll_for_event(xcb_connection_t *c);
xcb_generic_error_t *xcb_request_check(xcb_connection_t *c, xcb_void_cookie_t cookie);
void xcb_discard_reply(xcb_connection_t *c, unsigned int sequence);
const xcb_setup_t *xcb_get_setup(xcb_connection_t *c);
int xcb_get_file_descriptor(xcb_connection_t *c);
int xcb_connection_has_error(xcb_connection_t *c);
void xcb_disconnect(xcb_connection_t *c);
xcb_connection_t *xcb_connect(const char *displayname, int *screenp);
uint32_t xcb_generate_id(xcb_connection_t *c);

xcb_void_cookie_t
xcb_map_window (xcb_connection_t *c  /**< */,
                xcb_window_t      window  /**< */);
xcb_void_cookie_t
xcb_unmap_window (xcb_connection_t *c  /**< */,
                  xcb_window_t      window  /**< */);


xcb_void_cookie_t
xcb_change_window_attributes_checked (xcb_connection_t *c  /**< */,
                                      xcb_window_t      window  /**< */,
                                      uint32_t          value_mask  /**< */,
                                      const uint32_t   *value_list  /**< */);

xcb_void_cookie_t
xcb_change_window_attributes (xcb_connection_t *c  /**< */,
                              xcb_window_t      window  /**< */,
                              uint32_t          value_mask  /**< */,
                              const uint32_t   *value_list  /**< */);

xcb_void_cookie_t
xcb_configure_window (xcb_connection_t *c  /**< */,
                      xcb_window_t      window  /**< */,
                      uint16_t          value_mask  /**< */,
                      const uint32_t   *value_list  /**< */);

xcb_alloc_color_cookie_t
xcb_alloc_color (xcb_connection_t *c  /**< */,
                 xcb_colormap_t    cmap  /**< */,
                 uint16_t          red  /**< */,
                 uint16_t          green  /**< */,
                 uint16_t          blue  /**< */);

xcb_alloc_color_reply_t *
xcb_alloc_color_reply (xcb_connection_t          *c  /**< */,
                       xcb_alloc_color_cookie_t   cookie  /**< */,
                       xcb_generic_error_t      **e  /**< */);

xcb_alloc_named_color_cookie_t
xcb_alloc_named_color (xcb_connection_t *c  /**< */,
                       xcb_colormap_t    cmap  /**< */,
                       uint16_t          name_len  /**< */,
                       const char       *name  /**< */);

xcb_alloc_named_color_reply_t *
xcb_alloc_named_color_reply (xcb_connection_t                *c  /**< */,
                             xcb_alloc_named_color_cookie_t   cookie  /**< */,
                             xcb_generic_error_t            **e  /**< */);

xcb_void_cookie_t
xcb_set_input_focus (xcb_connection_t *c  /**< */,
                     uint8_t           revert_to  /**< */,
                     xcb_window_t      focus  /**< */,
                     xcb_timestamp_t   time  /**< */);


xcb_get_property_cookie_t
xcb_get_property (xcb_connection_t *c  /**< */,
                  uint8_t           _delete  /**< */,
                  xcb_window_t      window  /**< */,
                  xcb_atom_t        property  /**< */,
                  xcb_atom_t        type  /**< */,
                  uint32_t          long_offset  /**< */,
                  uint32_t          long_length  /**< */);

xcb_get_property_reply_t *
xcb_get_property_reply (xcb_connection_t           *c  /**< */,
                        xcb_get_property_cookie_t   cookie  /**< */,
                        xcb_generic_error_t       **e  /**< */);

void *
xcb_get_property_value (const xcb_get_property_reply_t *R  /**< */);

int
xcb_get_property_value_length (const xcb_get_property_reply_t *R  /**< */);


xcb_get_keyboard_mapping_cookie_t
xcb_get_keyboard_mapping (xcb_connection_t *c  /**< */,
                          xcb_keycode_t     first_keycode  /**< */,
                          uint8_t           count  /**< */);

xcb_get_keyboard_mapping_reply_t *
xcb_get_keyboard_mapping_reply (xcb_connection_t                   *c  /**< */,
                                xcb_get_keyboard_mapping_cookie_t   cookie  /**< */,
                                xcb_generic_error_t               **e  /**< */);

xcb_keysym_t *
xcb_get_keyboard_mapping_keysyms (const xcb_get_keyboard_mapping_reply_t *R  /**< */);

xcb_get_modifier_mapping_cookie_t
xcb_get_modifier_mapping (xcb_connection_t *c  /**< */);

xcb_get_modifier_mapping_reply_t *
xcb_get_modifier_mapping_reply (xcb_connection_t                   *c  /**< */,
                                xcb_get_modifier_mapping_cookie_t   cookie  /**< */,
                                xcb_generic_error_t               **e  /**< */);

xcb_keycode_t *
xcb_get_modifier_mapping_keycodes (const xcb_get_modifier_mapping_reply_t *R  /**< */);

xcb_void_cookie_t
xcb_grab_key_checked (xcb_connection_t *c  /**< */,
                      uint8_t           owner_events  /**< */,
                      xcb_window_t      grab_window  /**< */,
                      uint16_t          modifiers  /**< */,
                      xcb_keycode_t     key  /**< */,
                      uint8_t           pointer_mode  /**< */,
                      uint8_t           keyboard_mode  /**< */);

xcb_void_cookie_t
xcb_ungrab_key_checked (xcb_connection_t *c  /**< */,
                        xcb_keycode_t     key  /**< */,
                        xcb_window_t      grab_window  /**< */,
                        uint16_t          modifiers  /**< */);

xcb_void_cookie_t
xcb_create_window (xcb_connection_t *c  /**< */,
                   uint8_t           depth  /**< */,
                   xcb_window_t      wid  /**< */,
                   xcb_window_t      parent  /**< */,
                   int16_t           x  /**< */,
                   int16_t           y  /**< */,
                   uint16_t          width  /**< */,
                   uint16_t          height  /**< */,
                   uint16_t          border_width  /**< */,
                   uint16_t          _class  /**< */,
                   xcb_visualid_t    visual  /**< */,
                   uint32_t          value_mask  /**< */,
                   const uint32_t   *value_list  /**< */);

xcb_void_cookie_t
xcb_destroy_window (xcb_connection_t *c  /**< */,
                    xcb_window_t      window  /**< */);

xcb_get_window_attributes_cookie_t
xcb_get_window_attributes (xcb_connection_t *c  /**< */,
                           xcb_window_t      window  /**< */);

xcb_get_window_attributes_reply_t *
xcb_get_window_attributes_reply (xcb_connection_t                    *c  /**< */,
                                 xcb_get_window_attributes_cookie_t   cookie  /**< */,
                                 xcb_generic_error_t                **e  /**< */);

xcb_get_geometry_cookie_t
xcb_get_geometry (xcb_connection_t *c  /**< */,
                  xcb_drawable_t    drawable  /**< */);

xcb_get_geometry_reply_t *
xcb_get_geometry_reply (xcb_connection_t           *c  /**< */,
                        xcb_get_geometry_cookie_t   cookie  /**< */,
                        xcb_generic_error_t       **e  /**< */);

xcb_intern_atom_cookie_t
xcb_intern_atom (xcb_connection_t *c  /**< */,
                 uint8_t           only_if_exists  /**< */,
                 uint16_t          name_len  /**< */,
                 const char       *name  /**< */);

xcb_intern_atom_cookie_t
xcb_intern_atom_unchecked (xcb_connection_t *c  /**< */,
                           uint8_t           only_if_exists  /**< */,
                           uint16_t          name_len  /**< */,
                           const char       *name  /**< */);

xcb_intern_atom_reply_t *
xcb_intern_atom_reply (xcb_connection_t          *c  /**< */,
                       xcb_intern_atom_cookie_t   cookie  /**< */,
                       xcb_generic_error_t      **e  /**< */);


xcb_get_atom_name_cookie_t
xcb_get_atom_name (xcb_connection_t *c  /**< */,
                   xcb_atom_t        atom  /**< */);

xcb_get_atom_name_cookie_t
xcb_get_atom_name_unchecked (xcb_connection_t *c  /**< */,
                             xcb_atom_t        atom  /**< */);

xcb_void_cookie_t
xcb_kill_client (xcb_connection_t *c  /**< */,
                 uint32_t          resource  /**< */);

xcb_void_cookie_t
xcb_send_event (xcb_connection_t *c  /**< */,
                uint8_t           propagate  /**< */,
                xcb_window_t      destination  /**< */,
                uint32_t          event_mask  /**< */,
                const char       *event  /**< */);

xcb_void_cookie_t
xcb_create_pixmap (xcb_connection_t *c  /**< */,
                   uint8_t           depth  /**< */,
                   xcb_pixmap_t      pid  /**< */,
                   xcb_drawable_t    drawable  /**< */,
                   uint16_t          width  /**< */,
                   uint16_t          height  /**< */);

xcb_void_cookie_t
xcb_create_gc (xcb_connection_t *c  /**< */,
               xcb_gcontext_t    cid  /**< */,
               xcb_drawable_t    drawable  /**< */,
               uint32_t          value_mask  /**< */,
               const uint32_t   *value_list  /**< */);


xcb_void_cookie_t
xcb_free_pixmap (xcb_connection_t *c  /**< */,
                 xcb_pixmap_t      pixmap  /**< */);

xcb_void_cookie_t
xcb_free_gc (xcb_connection_t *c  /**< */,
             xcb_gcontext_t    gc  /**< */);

xcb_void_cookie_t
xcb_copy_area (xcb_connection_t *c  /**< */,
               xcb_drawable_t    src_drawable  /**< */,
               xcb_drawable_t    dst_drawable  /**< */,
               xcb_gcontext_t    gc  /**< */,
               int16_t           src_x  /**< */,
               int16_t           src_y  /**< */,
               int16_t           dst_x  /**< */,
               int16_t           dst_y  /**< */,
               uint16_t          width  /**< */,
               uint16_t          height  /**< */);


/*
 * xcb/xcb_aux.h
 */
uint8_t          xcb_aux_get_depth       (xcb_connection_t *c,
                                          xcb_screen_t     *screen);

uint8_t xcb_aux_get_depth_of_visual      (xcb_screen_t *screen,
                      xcb_visualid_t id);

xcb_screen_t     *xcb_aux_get_screen     (xcb_connection_t *c,
                                          int               screen);

xcb_visualtype_t *xcb_aux_get_visualtype (xcb_connection_t *c,
                                          int               screen,
                                          xcb_visualid_t    vid);

xcb_visualtype_t *
xcb_aux_find_visual_by_id (xcb_screen_t *screen,
               xcb_visualid_t id);

xcb_visualtype_t *
xcb_aux_find_visual_by_attrs (xcb_screen_t *screen,
                  int8_t class_,
                  int8_t depth);
"""

cairo = """
typedef struct _cairo cairo_t;

typedef struct _cairo_surface cairo_surface_t;
cairo_surface_t *
cairo_xcb_surface_create (xcb_connection_t	*connection,
			  xcb_drawable_t	 drawable,
			  xcb_visualtype_t	*visual,
			  int			 width,
			  int			 height);

cairo_t *
cairo_create (cairo_surface_t *target);

void
cairo_destroy (cairo_t *cr);

void
cairo_surface_destroy (cairo_surface_t *surface);

typedef enum _cairo_font_slant {
    CAIRO_FONT_SLANT_NORMAL,
    CAIRO_FONT_SLANT_ITALIC,
    CAIRO_FONT_SLANT_OBLIQUE
} cairo_font_slant_t;

typedef enum _cairo_font_weight {
    CAIRO_FONT_WEIGHT_NORMAL,
    CAIRO_FONT_WEIGHT_BOLD
} cairo_font_weight_t;


void
cairo_select_font_face (cairo_t              *cr,
			const char           *family,
			cairo_font_slant_t   slant,
			cairo_font_weight_t  weight);

void
cairo_set_font_size (cairo_t *cr, double size);

void
cairo_set_source_rgb (cairo_t *cr, double red, double green, double blue);

typedef enum _cairo_operator {
    CAIRO_OPERATOR_CLEAR,

    CAIRO_OPERATOR_SOURCE,
    CAIRO_OPERATOR_OVER,
    CAIRO_OPERATOR_IN,
    CAIRO_OPERATOR_OUT,
    CAIRO_OPERATOR_ATOP,

    CAIRO_OPERATOR_DEST,
    CAIRO_OPERATOR_DEST_OVER,
    CAIRO_OPERATOR_DEST_IN,
    CAIRO_OPERATOR_DEST_OUT,
    CAIRO_OPERATOR_DEST_ATOP,

    CAIRO_OPERATOR_XOR,
    CAIRO_OPERATOR_ADD,
    CAIRO_OPERATOR_SATURATE,

    CAIRO_OPERATOR_MULTIPLY,
    CAIRO_OPERATOR_SCREEN,
    CAIRO_OPERATOR_OVERLAY,
    CAIRO_OPERATOR_DARKEN,
    CAIRO_OPERATOR_LIGHTEN,
    CAIRO_OPERATOR_COLOR_DODGE,
    CAIRO_OPERATOR_COLOR_BURN,
    CAIRO_OPERATOR_HARD_LIGHT,
    CAIRO_OPERATOR_SOFT_LIGHT,
    CAIRO_OPERATOR_DIFFERENCE,
    CAIRO_OPERATOR_EXCLUSION,
    CAIRO_OPERATOR_HSL_HUE,
    CAIRO_OPERATOR_HSL_SATURATION,
    CAIRO_OPERATOR_HSL_COLOR,
    CAIRO_OPERATOR_HSL_LUMINOSITY
} cairo_operator_t;

void
cairo_set_operator (cairo_t *cr, cairo_operator_t op);

void
cairo_paint (cairo_t *cr);

typedef struct {
    double x_bearing;
    double y_bearing;
    double width;
    double height;
    double x_advance;
    double y_advance;
} cairo_text_extents_t;

typedef struct {
    double ascent;
    double descent;
    double height;
    double max_x_advance;
    double max_y_advance;
} cairo_font_extents_t;

void
cairo_text_extents (cairo_t              *cr,
		    const char    	 *utf8,
		    cairo_text_extents_t *extents);

void
cairo_font_extents (cairo_t              *cr,
		    cairo_font_extents_t *extents);

void
cairo_rectangle (cairo_t *cr,
		 double x, double y,
		 double width, double height);

void
cairo_stroke (cairo_t *cr);

void
cairo_fill (cairo_t *cr);

void
cairo_set_line_width (cairo_t *cr, double width);

void
cairo_move_to (cairo_t *cr, double x, double y);

void
cairo_show_text (cairo_t *cr, const char *utf8);

"""
