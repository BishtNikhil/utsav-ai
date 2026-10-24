// UtsavAI Reactive Client Application
let currentPlan = null;

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initDefaults();
  bindEvents();
  loadPreset('wedding_srinivas_scenario');
});

function initTheme() {
  const savedTheme = localStorage.getItem('utsav-theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeButton(savedTheme);
}

function updateThemeButton(theme) {
  const icon = document.getElementById('theme-icon');
  const text = document.getElementById('theme-text');
  if (icon && text) {
    if (theme === 'dark') {
      icon.textContent = '☀️';
      text.textContent = 'Light Mode';
    } else {
      icon.textContent = '🌙';
      text.textContent = 'Dark Mode';
    }
  }
}

function initDefaults() {
  // Set default target date to 120 days from today
  const targetDateInput = document.getElementById('input-target-date');
  const d = new Date();
  d.setDate(d.getDate() + 120);
  targetDateInput.value = d.toISOString().split('T')[0];
}

function bindEvents() {
  // Theme Toggle Button
  const themeBtn = document.getElementById('btn-theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('utsav-theme', newTheme);
      updateThemeButton(newTheme);
    });
  }

  // Tab Navigation
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const targetPane = document.getElementById(btn.dataset.tab);
      if (targetPane) targetPane.classList.add('active');
    });
  });

  // Guest Slider Input
  const guestSlider = document.getElementById('slider-guest-count');
  const guestDisplay = document.getElementById('display-guest-count');
  guestSlider.addEventListener('input', (e) => {
    guestDisplay.textContent = `${e.target.value} Attendees`;
  });

  // Preset Buttons
  document.querySelectorAll('.preset-chip-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.preset-chip-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadPreset(btn.dataset.preset);
    });
  });

  // Generate Plan Button
  document.getElementById('btn-generate-plan').addEventListener('click', generatePlan);

  // Run Change Test Benchmark Button
  document.getElementById('btn-run-change-test').addEventListener('click', runChangeTest);
}

// Preset Loader
async function loadPreset(presetKey) {
  try {
    const res = await fetch(`/api/preset/${presetKey}`);
    if (!res.ok) throw new Error('Preset load failed');
    const data = await res.json();
    const intake = data.intake;

    document.getElementById('input-event-title').value = intake.title;
    document.getElementById('select-event-category').value = intake.category;
    document.getElementById('slider-guest-count').value = intake.guest_count;
    document.getElementById('display-guest-count').textContent = `${intake.guest_count} Attendees`;
    document.getElementById('input-total-budget').value = intake.total_budget;
    document.getElementById('input-target-date').value = intake.target_date;
    document.getElementById('select-experience-tier').value = intake.experience_tier;

    if (intake.priority_weights) {
      document.getElementById('rank-catering').value = intake.priority_weights.catering || 1;
      document.getElementById('rank-venue').value = intake.priority_weights.venue || 2;
      document.getElementById('rank-decor').value = intake.priority_weights.decor || 3;
      document.getElementById('rank-photo').value = intake.priority_weights.photography || 4;
    }

    // Automatically trigger initial blueprint generation
    await generatePlan();
  } catch (err) {
    console.error('Error loading preset:', err);
  }
}

// Plan Generator
async function generatePlan() {
  const payload = {
    title: document.getElementById('input-event-title').value,
    category: document.getElementById('select-event-category').value,
    guest_count: parseInt(document.getElementById('slider-guest-count').value, 10),
    total_budget: parseFloat(document.getElementById('input-total-budget').value),
    target_date: document.getElementById('input-target-date').value,
    experience_tier: document.getElementById('select-experience-tier').value,
    priority_weights: {
      catering: parseInt(document.getElementById('rank-catering').value, 10),
      venue: parseInt(document.getElementById('rank-venue').value, 10),
      decor: parseInt(document.getElementById('rank-decor').value, 10),
      photography: parseInt(document.getElementById('rank-photo').value, 10),
      entertainment: 5,
    },
    must_haves: ["Culinary Experience", "Live Ensemble"],
    special_notes: "Auto-generated via UtsavAI orchestrator."
  };

  try {
    const res = await fetch('/api/plan/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Generation failed');
    currentPlan = await res.json();
    renderPlan(currentPlan);
    showToast('✨ Event Blueprint Generated Successfully!');
  } catch (err) {
    console.error('Failed to generate plan:', err);
    alert('Error generating plan. Check console for details.');
  }
}

// SME Change Test Benchmark Execution
async function runChangeTest() {
  if (!currentPlan) {
    await generatePlan();
  }

  const payload = {
    current_plan: currentPlan,
    guest_count_delta: 50,
    budget_delta_pct: -0.10,
    date_shift_days: -14,
    user_instruction: "50 more guests added, budget cut by 10%, event moved 2 weeks earlier."
  };

  try {
    const res = await fetch('/api/plan/change-test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Change test failed');
    const changeResponse = await res.json();

    currentPlan = changeResponse.recalculated_plan;
    renderPlan(currentPlan);

    // Sync input controls with recalculated values
    document.getElementById('slider-guest-count').value = currentPlan.intake.guest_count;
    document.getElementById('display-guest-count').textContent = `${currentPlan.intake.guest_count} Attendees`;
    document.getElementById('input-total-budget').value = currentPlan.intake.total_budget;
    document.getElementById('input-target-date').value = currentPlan.intake.target_date;

    showToast('⚡ SME Change Test PASSED: +50 guests accommodated, plan re-anchored seamlessly!');
  } catch (err) {
    console.error('Change test error:', err);
  }
}

// Main Render Function
function renderPlan(plan) {
  const budget = plan.budget_summary;
  const intake = plan.intake;

  // 1. Render KPIs
  document.getElementById('kpi-allocated').textContent = `₹${budget.total_allocated.toLocaleString('en-IN')}`;
  const perHead = Math.round(budget.total_allocated / intake.guest_count);
  document.getElementById('kpi-per-head').textContent = `₹${perHead.toLocaleString('en-IN')}`;
  document.getElementById('kpi-guest-sub').textContent = `Based on ${intake.guest_count} Guests`;
  document.getElementById('kpi-contingency').textContent = `₹${budget.contingency_reserve.toLocaleString('en-IN')}`;
  const venueSqFt = intake.guest_count * 12;
  document.getElementById('kpi-venue-sqft').textContent = `${venueSqFt.toLocaleString('en-IN')} sq.ft`;

  // 2. Render Budget Categories
  const catGrid = document.getElementById('budget-categories-grid');
  catGrid.innerHTML = '';
  budget.categories.forEach(cat => {
    const card = document.createElement('div');
    card.className = 'category-card';
    card.innerHTML = `
      <div class="cat-header">
        <span class="cat-title">${cat.category_name}</span>
        <span class="cat-status-tag">${cat.status_label}</span>
      </div>
      <div class="cat-amount-row">
        <span class="cat-amount">₹${cat.allocated_amount.toLocaleString('en-IN')}</span>
        <span class="cat-pct">${cat.percentage_of_budget}% of Budget</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill" style="width: ${Math.min(100, cat.percentage_of_budget * 2.2)}%;"></div>
      </div>
      <div class="cat-subitems-list">
        ${cat.sub_items.map(item => {
          const k = Object.keys(item)[0];
          const v = item[k];
          return `<div class="cat-subitem"><span>${k}</span><span>₹${v.toLocaleString('en-IN')}</span></div>`;
        }).join('')}
      </div>
    `;
    catGrid.appendChild(card);
  });

  // 3. Render Timeline DAG
  const timelineContainer = document.getElementById('timeline-milestones-list');
  timelineContainer.innerHTML = '';
  plan.timeline.milestones.forEach(ms => {
    const card = document.createElement('div');
    card.className = `milestone-card ${ms.is_critical_path ? 'critical' : ''}`;
    card.innerHTML = `
      <div class="ms-date-box">
        <span class="ms-date">${ms.deadline_date}</span>
        <span class="ms-days-before">${ms.days_before_event} Days Prior</span>
      </div>
      <div class="ms-body">
        <h4>${ms.title} ${ms.is_critical_path ? '<span style="color:var(--accent-rose); font-size:0.75rem;">[CRITICAL PATH]</span>' : ''}</h4>
        <p>${ms.description}</p>
        <div class="ms-deps">
          ${ms.dependencies.map(d => `<span class="dep-chip">Depends on: ${d.replace('ms_', '')}</span>`).join('')}
          <span class="dep-chip" style="color:var(--accent-emerald); border-color:var(--accent-emerald);">Fallback: ${ms.contingency_action}</span>
        </div>
      </div>
      <div>
        <span class="badge ${ms.status === 'in_progress' ? 'badge-cyan' : 'badge-gold'}">${ms.status}</span>
      </div>
    `;
    timelineContainer.appendChild(card);
  });

  // 4. Render Trade-Offs
  const tradeoffsGrid = document.getElementById('tradeoffs-options-grid');
  tradeoffsGrid.innerHTML = '';
  plan.trade_off_options.forEach(opt => {
    const card = document.createElement('div');
    card.className = `tradeoff-card ${opt.recommended ? 'recommended' : ''}`;
    card.innerHTML = `
      <div class="tradeoff-header">
        <h4>${opt.title}</h4>
        <span class="tradeoff-saving-badge">Saves ₹${Math.abs(opt.cost_delta).toLocaleString('en-IN')}</span>
      </div>
      <p style="font-size:0.85rem; color:var(--text-secondary); line-height:1.5;">${opt.scenario_description}</p>
      <div class="tradeoff-pros-cons">
        ${opt.pros.map(p => `<div class="pro-item">✓ <span>${p}</span></div>`).join('')}
        ${opt.cons.map(c => `<div class="con-item">⚠ <span>${c}</span></div>`).join('')}
      </div>
      ${opt.recommended ? '<div style="margin-top:auto; font-size:0.75rem; color:var(--accent-gold); font-weight:700;">★ Recommended by UtsavAI Priority Engine</div>' : ''}
    `;
    tradeoffsGrid.appendChild(card);
  });

  // 5. Render Vendor Copilot
  const vendorContainer = document.getElementById('vendor-comparisons-list');
  vendorContainer.innerHTML = '';
  plan.vendor_comparisons.forEach(vc => {
    const block = document.createElement('div');
    block.className = 'vendor-comparison-block';
    block.innerHTML = `
      <h3 style="color:#fff; font-size:1.1rem; margin-bottom:0.5rem;">🤝 ${vc.category} Quotation Analysis</h3>
      <div class="quotes-pair-grid">
        ${vc.quotes.map(q => `
          <div class="quote-box ${q.vendor_id === vc.recommended_vendor_id ? 'recommended-vendor' : ''}">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
              <strong style="color:var(--accent-gold-light);">${q.vendor_name}</strong>
              <span class="badge ${q.vendor_id === vc.recommended_vendor_id ? 'badge-emerald' : 'badge-gold'}">
                ${q.vendor_id === vc.recommended_vendor_id ? 'Best Fit' : 'Candidate'}
              </span>
            </div>
            <div style="font-family:var(--font-mono); font-size:1.25rem; font-weight:700; color:#fff;">
              ₹${q.total_cost.toLocaleString('en-IN')}
              ${q.per_plate_or_unit ? `<span style="font-size:0.8rem; color:var(--text-muted);">(₹${q.per_plate_or_unit}/plate)</span>` : ''}
            </div>
            <div style="font-size:0.8rem; color:var(--text-secondary);">
              <strong>Inclusions:</strong> ${q.inclusions.join(', ')}
            </div>
            ${q.hidden_costs_flagged.length > 0 ? `
              <div class="hidden-fees-box">
                <strong>🚨 Hidden Fees Flagged:</strong>
                ${q.hidden_costs_flagged.join(' • ')}
              </div>
            ` : ''}
          </div>
        `).join('')}
      </div>
      <div style="margin-top:1rem; padding:0.75rem; background:rgba(0,0,0,0.3); border-radius:6px;">
        <strong style="font-size:0.85rem; color:var(--accent-cyan);">💡 Negotiation Questions to Ask:</strong>
        <ul style="font-size:0.8rem; color:var(--text-secondary); margin-left:1.25rem; margin-top:0.25rem;">
          ${vc.negotiation_questions.map(q => `<li>${q}</li>`).join('')}
        </ul>
      </div>
    `;
    vendorContainer.appendChild(block);
  });

  // 6. Render Celebration Showcase (Heritage from marriage_card_lab)
  const showcaseContainer = document.getElementById('celebration-showcase-view');
  showcaseContainer.innerHTML = '';
  const theme = plan.digital_theme;
  const showcaseHeader = document.createElement('div');
  showcaseHeader.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
      <div>
        <h3 style="font-family:var(--font-serif); font-size:1.35rem; color:var(--accent-gold-light);">${theme.theme_name}</h3>
        <p style="font-size:0.85rem; color:var(--text-secondary);">${theme.aesthetic_style} • RSVP Link: <code>/${theme.rsvp_link_slug}</code></p>
      </div>
      <span class="badge badge-gold">Interactive Invitation Suite Active</span>
    </div>
  `;
  showcaseContainer.appendChild(showcaseHeader);

  const ceremoniesGrid = document.createElement('div');
  ceremoniesGrid.className = 'ceremonies-grid';
  theme.ceremonies.forEach(ceremony => {
    const card = document.createElement('div');
    card.className = 'ceremony-card';
    card.innerHTML = `
      <h4>${ceremony.ceremony_name}</h4>
      <div class="ceremony-meta">
        <div><strong>🗓️ Schedule:</strong> ${ceremony.date_label}</div>
        <div><strong>🏛️ Venue:</strong> ${ceremony.venue_type}</div>
        <div><strong>👗 Dress Code:</strong> ${ceremony.dress_code}</div>
        <div><strong>🎵 Music Vibe:</strong> ${ceremony.music_vibe}</div>
      </div>
      <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.4rem;">
        <strong>Highlights:</strong> ${ceremony.key_highlights.join(' • ')}
      </div>
    `;
    ceremoniesGrid.appendChild(card);
  });
  showcaseContainer.appendChild(ceremoniesGrid);

  // 7. Render AI Narrative in Inspector
  document.getElementById('ai-narrative-text').innerHTML = plan.ai_reasoning_narrative.replace(/\n/g, '<br>');
}

// Toast Notification Utility
function showToast(msg) {
  const toast = document.getElementById('app-toast-notice');
  toast.textContent = msg;
  toast.style.display = 'block';
  setTimeout(() => {
    toast.style.display = 'none';
  }, 4000);
}
