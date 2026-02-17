#define DISTANCIA_ARRASTO 10

#define LIMIAR_BRILHO 0.05f 

float get_luma(uchar r, uchar g, uchar b) {
    return ((float)r * 0.299f + (float)g * 0.587f + (float)b * 0.114f) / 255.0f;
}

uchar3 read_safe_pixel(__global const unsigned char* src, int x, int y, int width, int height) {
    int sx = clamp(x, 0, width - 1);
    int sy = clamp(y, 0, height - 1);
    int idx = (sy * width + sx) * 3;
    return (uchar3)(src[idx], src[idx+1], src[idx+2]);
}

__kernel void process_image(
    __global const unsigned char* src, 
    __global unsigned char* dst, 
    int width, 
    int height
) {
    int idx = get_global_id(0);
    if (idx >= width * height) return;

    int x = idx % width;
    int y = idx / width;

    uchar3 pixel_atual = read_safe_pixel(src, x, y, width, height);
    float luma_atual = get_luma(pixel_atual.x, pixel_atual.y, pixel_atual.z);

    int melhor_xr = x;
    float melhor_luma_r = luma_atual;
    
    int direcao_r = (y % 2 == 0) ? -1 : 1;

    for (int i = 1; i <= DISTANCIA_ARRASTO; i++) {
        int vizinho_x = x + (i * direcao_r);
        uchar3 p_viz = read_safe_pixel(src, vizinho_x, y, width, height);
        float luma_viz = get_luma(p_viz.x, p_viz.y, p_viz.z);

        if (luma_viz > melhor_luma_r + LIMIAR_BRILHO) {
            melhor_luma_r = luma_viz;
            melhor_xr = vizinho_x;
        }
    }
    uchar final_r = read_safe_pixel(src, melhor_xr, y, width, height).x;

    int melhor_yg = y;
    float melhor_luma_g = luma_atual;

    int direcao_g = (x % 2 == 0) ? -1 : 1;

    for (int i = 1; i <= DISTANCIA_ARRASTO; i++) {
        int vizinho_y = y + (i * direcao_g);
        uchar3 p_viz = read_safe_pixel(src, x, vizinho_y, width, height);
        float luma_viz = get_luma(p_viz.x, p_viz.y, p_viz.z);

        if (luma_viz > melhor_luma_g + LIMIAR_BRILHO) {
            melhor_luma_g = luma_viz;
            melhor_yg = vizinho_y;
        }
    }
    uchar final_g = read_safe_pixel(src, x, melhor_yg, width, height).y;

    float noise = sin(dot((float2)(x,y), (float2)(12.9898f,78.233f))) * 43758.5453f;
    noise = noise - floor(noise); // Fica entre 0.0 e 1.0
    
    int azul_ruidoso = (int)pixel_atual.z + (int)((noise - 0.5f) * 40.0f);
    uchar final_b = (uchar)clamp(azul_ruidoso, 0, 255);

    dst[idx*3 + 0] = final_r;
    dst[idx*3 + 1] = final_g;
    dst[idx*3 + 2] = final_b;
}
