// Manipulation Detection API
// Identify manipulation patterns in text using Pattern Theory

export default async (request, context) => {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const { text, context: textContext } = await request.json();

    if (!text) {
      return new Response(JSON.stringify({ error: 'text required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const analysis = detectManipulation(text, textContext);

    return new Response(JSON.stringify(analysis), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

function detectManipulation(text, textContext) {
  const lowerText = text.toLowerCase();

  // DESTROYER PATTERNS
  const destroyerPatterns = {
    authority_appeal: [
      'expert', 'doctor', 'scientist', 'studies show', 'research proves',
      'authorities', 'official'
    ],
    fear_mongering: [
      'danger', 'risk', 'warning', 'urgent', 'crisis', 'emergency',
      'threat', 'before it\'s too late'
    ],
    scarcity_pressure: [
      'limited time', 'act now', 'only', 'exclusive', 'last chance',
      'running out', 'deadline'
    ],
    social_proof: [
      'everyone', 'most people', 'millions', 'trending', 'viral',
      'popular', 'they all'
    ],
    emotional_appeal: [
      'feel', 'love', 'hate', 'fear', 'angry', 'sad', 'happy',
      'excited', 'worried'
    ],
    false_dichotomy: [
      'either', 'or else', 'only two', 'must choose', 'no other option',
      'black and white'
    ],
    gaslighting: [
      'you\'re crazy', 'that never happened', 'you\'re imagining',
      'you always', 'you never', 'everyone thinks you'
    ],
    guilt_manipulation: [
      'after all i\'ve done', 'how could you', 'you owe me',
      'disappointed', 'let down', 'ungrateful'
    ]
  };

  // Detect each pattern
  const detected = {};
  let totalScore = 0;
  let detectedPatterns = [];

  for (const [pattern, indicators] of Object.entries(destroyerPatterns)) {
    const found = indicators.filter(ind => lowerText.includes(ind));
    if (found.length > 0) {
      detected[pattern] = {
        count: found.length,
        examples: found.slice(0, 3),
        severity: getSeverity(found.length)
      };
      totalScore += found.length * 10;
      detectedPatterns.push(pattern);
    }
  }

  // Calculate manipulation score (0-100)
  const manipulationScore = Math.min(100, totalScore);

  // Determine threat level
  let threatLevel, recommendation;
  if (manipulationScore >= 70) {
    threatLevel = 'HIGH';
    recommendation = 'Strong manipulation detected. Apply Pattern Theory neutralization protocols.';
  } else if (manipulationScore >= 40) {
    threatLevel = 'MEDIUM';
    recommendation = 'Moderate manipulation. Verify claims independently before acting.';
  } else if (manipulationScore > 0) {
    threatLevel = 'LOW';
    recommendation = 'Minor manipulation indicators. Stay aware but no immediate concern.';
  } else {
    threatLevel = 'CLEAR';
    recommendation = 'No significant manipulation patterns detected.';
  }

  // Neutralization protocols
  const neutralization = [];
  if (detected.authority_appeal) {
    neutralization.push('Verify credentials and check for conflicts of interest');
  }
  if (detected.fear_mongering) {
    neutralization.push('Research actual statistics and base rates');
  }
  if (detected.scarcity_pressure) {
    neutralization.push('Pause and recognize artificial urgency');
  }
  if (detected.social_proof) {
    neutralization.push('Question sample sizes and selection bias');
  }
  if (detected.gaslighting) {
    neutralization.push('Document facts and trust your observations');
  }
  if (detected.guilt_manipulation) {
    neutralization.push('Recognize emotional leverage and set boundaries');
  }

  return {
    text_length: text.length,
    manipulation_score: manipulationScore,
    threat_level: threatLevel,
    patterns_detected: detectedPatterns.length,
    detected_patterns: detected,
    neutralization_protocols: neutralization,
    recommendation: recommendation,
    immunity_boost: `Awareness of ${detectedPatterns.length} patterns increases manipulation immunity`,
    pattern_theory_formula: 'MS = Σ(pattern_count × 10)',
    timestamp: new Date().toISOString()
  };
}

function getSeverity(count) {
  if (count >= 3) return 'HIGH';
  if (count >= 2) return 'MEDIUM';
  return 'LOW';
}

export const config = {
  path: "/api/manipulation-detector"
};
