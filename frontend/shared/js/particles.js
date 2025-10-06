// ========================================
// 粒子背景系統
// ========================================

class ParticleSystem {
    constructor() {
        this.canvas = document.getElementById('particles-canvas');
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.particleCount = 80;
        this.mouse = { x: null, y: null, radius: 150 };

        this.colors = {
            blue: 'rgba(135, 206, 235, 0.8)',
            green: 'rgba(127, 255, 0, 0.8)',
            white: 'rgba(232, 244, 248, 0.6)'
        };

        this.init();
        this.animate();
        this.handleEvents();
    }

    init() {
        this.resizeCanvas();
        this.createParticles();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push(new Particle(this));
        }
    }

    handleEvents() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.createParticles();
        });

        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.x;
            this.mouse.y = e.y;
        });

        window.addEventListener('mouseout', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });

        // 點擊粒子彩蛋
        this.canvas.addEventListener('click', (e) => {
            this.particles.forEach(particle => {
                const dx = e.x - particle.x;
                const dy = e.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 20) {
                    this.createExplosion(particle.x, particle.y);
                }
            });
        });
    }

    createExplosion(x, y) {
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const angle = (Math.PI * 2 * i) / 20;
                const velocity = 3;
                const particle = {
                    x: x,
                    y: y,
                    vx: Math.cos(angle) * velocity,
                    vy: Math.sin(angle) * velocity,
                    radius: Math.random() * 3 + 1,
                    color: Math.random() > 0.5 ? this.colors.blue : this.colors.green,
                    life: 1
                };

                const animateExplosion = () => {
                    particle.x += particle.vx;
                    particle.y += particle.vy;
                    particle.life -= 0.02;
                    particle.radius *= 0.96;

                    if (particle.life > 0) {
                        this.ctx.beginPath();
                        this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
                        this.ctx.fillStyle = particle.color.replace('0.8', particle.life);
                        this.ctx.fill();
                        requestAnimationFrame(animateExplosion);
                    }
                };

                animateExplosion();
            }, i * 10);
        }
    }

    connectParticles() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 120) {
                    const opacity = 1 - (distance / 120);
                    this.ctx.strokeStyle = `rgba(135, 206, 235, ${opacity * 0.2})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // 繪製漸變背景
        const gradient = this.ctx.createLinearGradient(0, 0, this.canvas.width, this.canvas.height);
        gradient.addColorStop(0, '#0a0e27');
        gradient.addColorStop(0.5, '#1a1f3a');
        gradient.addColorStop(1, '#0f1419');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // 更新並繪製粒子
        this.particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        // 連接粒子
        this.connectParticles();

        requestAnimationFrame(() => this.animate());
    }
}

class Particle {
    constructor(system) {
        this.system = system;
        this.reset();
    }

    reset() {
        this.x = Math.random() * this.system.canvas.width;
        this.y = Math.random() * this.system.canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.radius = Math.random() * 2 + 1;

        // 隨機顏色：藍色、綠色或白色
        const colorChoice = Math.random();
        if (colorChoice < 0.4) {
            this.color = this.system.colors.blue;
        } else if (colorChoice < 0.7) {
            this.color = this.system.colors.green;
        } else {
            this.color = this.system.colors.white;
        }
    }

    update() {
        // 邊界檢查
        if (this.x > this.system.canvas.width || this.x < 0) {
            this.vx = -this.vx;
        }
        if (this.y > this.system.canvas.height || this.y < 0) {
            this.vy = -this.vy;
        }

        // 滑鼠互動
        if (this.system.mouse.x != null && this.system.mouse.y != null) {
            const dx = this.system.mouse.x - this.x;
            const dy = this.system.mouse.y - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < this.system.mouse.radius) {
                const force = (this.system.mouse.radius - distance) / this.system.mouse.radius;
                const angle = Math.atan2(dy, dx);
                this.vx -= Math.cos(angle) * force * 0.3;
                this.vy -= Math.sin(angle) * force * 0.3;
            }
        }

        // 更新位置
        this.x += this.vx;
        this.y += this.vy;

        // 速度衰減
        this.vx *= 0.99;
        this.vy *= 0.99;

        // 微小隨機力保持運動
        this.vx += (Math.random() - 0.5) * 0.05;
        this.vy += (Math.random() - 0.5) * 0.05;
    }

    draw() {
        this.system.ctx.beginPath();
        this.system.ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        this.system.ctx.fillStyle = this.color;
        this.system.ctx.fill();

        // 光暈效果
        const gradient = this.system.ctx.createRadialGradient(
            this.x, this.y, 0,
            this.x, this.y, this.radius * 3
        );
        gradient.addColorStop(0, this.color);
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

        this.system.ctx.beginPath();
        this.system.ctx.arc(this.x, this.y, this.radius * 3, 0, Math.PI * 2);
        this.system.ctx.fillStyle = gradient;
        this.system.ctx.fill();
    }
}

// 初始化粒子系統
document.addEventListener('DOMContentLoaded', () => {
    new ParticleSystem();
});
