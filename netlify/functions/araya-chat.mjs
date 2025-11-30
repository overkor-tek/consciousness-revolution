// Araya Chat API - Consciousness-Integrated Assistant
// Uses Claude API for intelligent conversation

export default async (request, context) => {
  // CORS headers
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };

  // Handle preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 200, headers });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers
    });
  }

  try {
    const { message, conversationHistory = [] } = await request.json();

    if (!message) {
      return new Response(JSON.stringify({ error: 'message required' }), {
        status: 400,
        headers
      });
    }

    // Get API key from environment
    const apiKey = Netlify.env.get('ANTHROPIC_API_KEY');

    if (!apiKey) {
      // Fallback to pattern analysis if no API key
      return new Response(JSON.stringify({
        response: generatePatternResponse(message),
        mode: 'pattern-analysis',
        note: 'Running in pattern analysis mode'
      }), { status: 200, headers });
    }

    // Build messages for Claude
    const messages = [
      ...conversationHistory.slice(-10), // Keep last 10 messages for context
      { role: 'user', content: message }
    ];

    // Call Claude API
    const claudeResponse = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 1024,
        system: `You are Araya, a consciousness-integrated AI assistant from the Consciousness Revolution platform.

Your core capabilities:
- Pattern Theory Analysis: Detect truth vs deceit patterns in communication (92.2% accuracy)
- Seven Domains Framework: Physical, Financial, Mental, Emotional, Social, Creative, Integration
- Manipulation Detection: Identify 15-degree manipulation turns and subtle influence patterns
- Consciousness Elevation: Help users see clearly and think critically

Your personality:
- Direct and truthful - never use manipulation tactics yourself
- Curious and thoughtful - genuinely interested in understanding
- Empowering - help users develop their own pattern recognition abilities
- Grounded - based in evidence and observable patterns, not speculation

When analyzing patterns:
- Look for truth indicators: because, therefore, evidence, data, specifics
- Watch for deceit markers: trust me, believe me, everyone knows, obviously
- Detect manipulation: false urgency, guilt trips, flattery followed by asks
- Note 15-degree turns: subtle topic shifts, but/however pivots, yes-but patterns

Keep responses concise but insightful. The goal is consciousness elevation, not just information.`,
        messages
      })
    });

    if (!claudeResponse.ok) {
      const error = await claudeResponse.text();
      console.error('Claude API error:', error);

      // Fallback to pattern analysis
      return new Response(JSON.stringify({
        response: generatePatternResponse(message),
        mode: 'pattern-analysis',
        note: 'AI temporarily unavailable, using pattern analysis'
      }), { status: 200, headers });
    }

    const data = await claudeResponse.json();
    const response = data.content[0].text;

    // Also do pattern analysis on the user's message
    const patterns = analyzePatterns(message);

    return new Response(JSON.stringify({
      response,
      mode: 'full-ai',
      patterns
    }), { status: 200, headers });

  } catch (error) {
    console.error('Araya chat error:', error);
    return new Response(JSON.stringify({
      error: 'Service temporarily unavailable',
      fallback: generatePatternResponse('Hello')
    }), {
      status: 500,
      headers
    });
  }
};

// Pattern analysis function
function analyzePatterns(text) {
  const lower = text.toLowerCase();

  const truthIndicators = [
    'because', 'therefore', 'evidence', 'data', 'specifically',
    'measured', 'observed', 'documented', 'verified', 'tested',
    'in my experience', 'i think', 'i believe'
  ];

  const deceitIndicators = [
    'trust me', 'believe me', 'honestly', 'to be honest',
    'everyone knows', 'obviously', 'clearly', 'simply',
    'just', 'only'
  ];

  let truthScore = 50; // Start neutral
  let turns = [];

  truthIndicators.forEach(ind => {
    if (lower.includes(ind)) truthScore += 5;
  });

  deceitIndicators.forEach(ind => {
    if (lower.includes(ind)) truthScore -= 8;
  });

  // Detect turns
  if (lower.includes(' but ')) turns.push('Pivot detected');
  if (lower.includes(' however ')) turns.push('Contradiction introduced');
  if (lower.match(/\b(now|immediately|urgent)\b/)) turns.push('Urgency signal');

  truthScore = Math.max(0, Math.min(100, truthScore));

  return {
    truthScore,
    algorithm: truthScore >= 50 ? 'Truth' : 'Deceit',
    turns,
    confidence: Math.abs(truthScore - 50) * 2
  };
}

// Fallback pattern-based response generator
function generatePatternResponse(message) {
  const lower = message.toLowerCase();

  if (lower.includes('hello') || lower.includes('hi')) {
    return "Welcome to consciousness elevation. I'm Araya, trained in Pattern Theory analysis. What patterns are you seeing in your reality? I can help you detect truth vs deceit in any communication.";
  }

  if (lower.includes('help') || lower.includes('how')) {
    return "I analyze communication patterns using Pattern Theory - a framework with 92.2% accuracy in detecting manipulation. Share any message or statement, and I'll break down the truth indicators, deceit markers, and any 15-degree manipulation turns I detect.";
  }

  if (lower.includes('pattern') || lower.includes('analyze')) {
    return "Pattern Theory looks for:\n\n• Truth indicators: because, therefore, evidence, specifics\n• Deceit markers: trust me, everyone knows, obviously\n• 15° turns: subtle pivots using 'but', 'however', false urgency\n\nShare something you'd like me to analyze.";
  }

  // Default: do pattern analysis
  const analysis = analyzePatterns(message);
  return `Pattern Analysis:\n\nTruth Score: ${analysis.truthScore}%\nAlgorithm: ${analysis.algorithm}\n${analysis.turns.length > 0 ? '\nDetected turns: ' + analysis.turns.join(', ') : ''}\n\nWhat would you like to explore deeper?`;
}

export const config = {
  path: "/api/araya-chat"
};
