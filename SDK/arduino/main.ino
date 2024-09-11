#include <stdint.h>
#include <servo.h>

typedef struct _position_t {
    uint8_t x;
    uint8_t y;
} position_t;

position_t current_pos;
position_t requested_pos;

void process_request(position_t *prequested_pos, String msg)
{
    prequested_pos->x;
}

void setup()
{
    
}

void loop()
{

}
