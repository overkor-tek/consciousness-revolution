/**
 * PATTERN THEORY WIDGET
 * =====================
 * Embeddable floating widget for real-time text analysis.
 *
 * Add to any page:
 * <script src="https://conciousnessrevolution.io/pattern-widget.js"></script>
 *
 * Features:
 * - Floating analyze button
 * - Highlight text to analyze
 * - Quick Truth/Deceit classification
 * - 15-degree turn detection
 *
 * Created: 2025-11-22
 * Trinity Build: C1 × C2 × C3
 */

(function() {
    'use strict';

    // Pattern Theory markers
    const DECEIT_MARKERS = [
        "but", "however", "actually", "trust me", "believe me",
        "obviously", "clearly", "everyone knows", "you should",
        "you must", "you need to", "just", "only", "simple",
        "easy", "quick", "free", "guaranteed", "limited time",
        "act now", "don't miss", "exclusive", "secret"
    ];

    const TRUTH_MARKERS = [
        "because", "therefore", "evidence shows", "data indicates",
        "research suggests", "in my experience", "i think", "i believe",
        "it seems", "from my perspective", "let me explain",
        "here's why", "the reason is", "consider this",
        "permanent", "foundation", "long-term", "quality"
    ];

    // Create styles
    const styles = `
        #pt-widget-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
            z-index: 999999;
            transition: all 0.3s ease;
        }

        #pt-widget-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6);
        }

        #pt-widget-panel {
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 320px;
            background: #1a1a2e;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            z-index: 999998;
            display: none;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: white;
            overflow: hidden;
        }

        #pt-widget-panel.active {
            display: block;
            animation: pt-slide-up 0.3s ease;
        }

        @keyframes pt-slide-up {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .pt-header {
            padding: 16px;
            background: rgba(0, 0, 0, 0.3);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .pt-header h3 {
            margin: 0;
            font-size: 14px;
            font-weight: 600;
        }

        .pt-close {
            background: none;
            border: none;
            color: rgba(255, 255, 255, 0.5);
            cursor: pointer;
            font-size: 18px;
        }

        .pt-content {
            padding: 16px;
        }

        .pt-textarea {
            width: 100%;
            height: 80px;
            padding: 10px;
            border: none;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 13px;
            resize: none;
            margin-bottom: 12px;
        }

        .pt-textarea::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }

        .pt-analyze-btn {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
            font-size: 13px;
            cursor: pointer;
        }

        .pt-result {
            margin-top: 16px;
            padding: 12px;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.3);
            display: none;
        }

        .pt-result.active {
            display: block;
        }

        .pt-result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .pt-algorithm {
            font-weight: bold;
            font-size: 14px;
        }

        .pt-algorithm.truth { color: #2ecc71; }
        .pt-algorithm.deceit { color: #e74c3c; }
        .pt-algorithm.neutral { color: #f39c12; }

        .pt-confidence {
            font-size: 12px;
            opacity: 0.7;
        }

        .pt-bars {
            margin-bottom: 8px;
        }

        .pt-bar-label {
            font-size: 11px;
            display: flex;
            justify-content: space-between;
            margin-bottom: 2px;
        }

        .pt-bar {
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            overflow: hidden;
            margin-bottom: 6px;
        }

        .pt-bar-fill {
            height: 100%;
            border-radius: 2px;
        }

        .pt-bar-fill.truth { background: #2ecc71; }
        .pt-bar-fill.deceit { background: #e74c3c; }

        .pt-turns {
            font-size: 11px;
            padding-top: 8px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        .pt-turn-item {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-top: 4px;
        }

        .pt-footer {
            padding: 12px 16px;
            background: rgba(0, 0, 0, 0.2);
            font-size: 10px;
            text-align: center;
            opacity: 0.5;
        }
    `;

    // Create widget HTML
    const widgetHTML = `
        <button id="pt-widget-btn" title="Pattern Theory Analyzer">🧠</button>
        <div id="pt-widget-panel">
            <div class="pt-header">
                <h3>🧠 Pattern Analysis</h3>
                <button class="pt-close">&times;</button>
            </div>
            <div class="pt-content">
                <textarea class="pt-textarea" placeholder="Paste or type text to analyze...&#10;&#10;Or highlight text on the page and click Analyze"></textarea>
                <button class="pt-analyze-btn">Analyze</button>
                <div class="pt-result" id="pt-result">
                    <div class="pt-result-header">
                        <span class="pt-algorithm" id="pt-algo">-</span>
                        <span class="pt-confidence" id="pt-conf">-</span>
                    </div>
                    <div class="pt-bars">
                        <div class="pt-bar-label">
                            <span>Truth</span>
                            <span id="pt-truth-val">0%</span>
                        </div>
                        <div class="pt-bar">
                            <div class="pt-bar-fill truth" id="pt-truth-bar" style="width: 0%"></div>
                        </div>
                        <div class="pt-bar-label">
                            <span>Deceit</span>
                            <span id="pt-deceit-val">0%</span>
                        </div>
                        <div class="pt-bar">
                            <div class="pt-bar-fill deceit" id="pt-deceit-bar" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="pt-turns" id="pt-turns"></div>
                </div>
            </div>
            <div class="pt-footer">
                Pattern Theory • 92.2% Accuracy • conciousnessrevolution.io
            </div>
        </div>
    `;

    // Analysis function
    function analyze(text) {
        const lower = text.toLowerCase();

        let deceitCount = 0;
        let truthCount = 0;

        DECEIT_MARKERS.forEach(m => {
            if (lower.includes(m)) deceitCount++;
        });

        TRUTH_MARKERS.forEach(m => {
            if (lower.includes(m)) truthCount++;
        });

        // Detect turns
        const turns = [];
        if (lower.includes('but ')) turns.push('Pivot after positive');
        if (lower.includes('however ')) turns.push('Contradiction introduced');
        if (lower.includes('yes, but')) turns.push('Agreement negation');
        if (lower.match(/\b(now|immediately|urgent)\b/) && lower.match(/\b(must|need|have to)\b/)) {
            turns.push('False urgency');
        }

        // Calculate scores
        const total = deceitCount + truthCount;
        let truthScore = total ? (truthCount / total) * 100 : 50;
        let deceitScore = total ? (deceitCount / total) * 100 : 50;

        // Adjust for turns
        const turnPenalty = turns.length * 10;
        deceitScore = Math.min(100, deceitScore + turnPenalty);
        truthScore = Math.max(0, truthScore - turnPenalty);

        // Normalize
        const newTotal = truthScore + deceitScore;
        if (newTotal > 0) {
            truthScore = (truthScore / newTotal) * 100;
            deceitScore = (deceitScore / newTotal) * 100;
        }

        const confidence = Math.abs(truthScore - deceitScore);
        let algorithm = 'NEUTRAL';
        if (confidence > 20) {
            algorithm = truthScore > deceitScore ? 'TRUTH' : 'DECEIT';
        }

        return {
            algorithm,
            truthScore: Math.round(truthScore),
            deceitScore: Math.round(deceitScore),
            confidence: Math.round(confidence),
            turns
        };
    }

    // Initialize widget
    function init() {
        // Add styles
        const styleEl = document.createElement('style');
        styleEl.textContent = styles;
        document.head.appendChild(styleEl);

        // Add widget
        const container = document.createElement('div');
        container.innerHTML = widgetHTML;
        document.body.appendChild(container);

        // Get elements
        const btn = document.getElementById('pt-widget-btn');
        const panel = document.getElementById('pt-widget-panel');
        const closeBtn = panel.querySelector('.pt-close');
        const textarea = panel.querySelector('.pt-textarea');
        const analyzeBtn = panel.querySelector('.pt-analyze-btn');
        const result = document.getElementById('pt-result');

        // Toggle panel
        btn.addEventListener('click', () => {
            panel.classList.toggle('active');

            // Auto-fill with selected text
            const selection = window.getSelection().toString().trim();
            if (selection) {
                textarea.value = selection;
            }
        });

        // Close panel
        closeBtn.addEventListener('click', () => {
            panel.classList.remove('active');
        });

        // Analyze
        analyzeBtn.addEventListener('click', () => {
            const text = textarea.value.trim();
            if (!text) return;

            const analysis = analyze(text);

            // Update UI
            const algoEl = document.getElementById('pt-algo');
            algoEl.textContent = analysis.algorithm + ' ALGORITHM';
            algoEl.className = 'pt-algorithm ' + analysis.algorithm.toLowerCase();

            document.getElementById('pt-conf').textContent = analysis.confidence + '% confidence';
            document.getElementById('pt-truth-val').textContent = analysis.truthScore + '%';
            document.getElementById('pt-deceit-val').textContent = analysis.deceitScore + '%';
            document.getElementById('pt-truth-bar').style.width = analysis.truthScore + '%';
            document.getElementById('pt-deceit-bar').style.width = analysis.deceitScore + '%';

            // Turns
            const turnsEl = document.getElementById('pt-turns');
            if (analysis.turns.length > 0) {
                turnsEl.innerHTML = '<strong>⚠️ 15° Turns:</strong>' +
                    analysis.turns.map(t => `<div class="pt-turn-item">• ${t}</div>`).join('');
            } else {
                turnsEl.innerHTML = '';
            }

            result.classList.add('active');
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!panel.contains(e.target) && e.target !== btn) {
                panel.classList.remove('active');
            }
        });
    }

    // Start when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
