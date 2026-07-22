import re

with open('src/components/DashboardAdmin.tsx', 'r') as f:
    content = f.read()

# Add recharts imports
import_statement = "import { motion, AnimatePresence } from \"motion/react\";"
new_import_statement = """import { motion, AnimatePresence } from "motion/react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie } from "recharts";
"""
content = content.replace(import_statement, new_import_statement)

# Add pagination state
state_pattern = r'  const \[viewMode, setViewMode\] = useState<"table" \| "grid">.*\n'
new_state = """  const [viewMode, setViewMode] = useState<"table" | "grid">("table");
  const [visibleCount, setVisibleCount] = useState(20);
"""
content = re.sub(state_pattern, new_state, content)

# Calculate chart data
calc_pattern = r'  const pendingAccCount = athletes\.filter\(\(a\) => !a\.isAcc\)\.length;'
new_calc = """  const pendingAccCount = athletes.filter((a) => !a.isAcc).length;

  const categoryStats = athletes.reduce((acc: any, athlete) => {
    const cat = athlete.kategori || 'Lainnya';
    if (!acc[cat]) acc[cat] = { name: cat, Putra: 0, Putri: 0, Total: 0 };
    if (athlete.jk === 'Putra') acc[cat].Putra++;
    if (athlete.jk === 'Putri') acc[cat].Putri++;
    acc[cat].Total++;
    return acc;
  }, {});
  const chartData = Object.values(categoryStats).sort((a: any, b: any) => b.Total - a.Total);

  const genderData = [
    { name: 'Putra', value: athletes.filter(a => a.jk === 'Putra').length, color: '#3b82f6' },
    { name: 'Putri', value: athletes.filter(a => a.jk === 'Putri').length, color: '#ec4899' }
  ];
"""
content = content.replace(calc_pattern, new_calc)

# Insert charts section
charts_insert_point = r'      </div>\s*\{\/\* Action panel - Refresh \*\/\}'
charts_markup = """      </div>

      {/* DASHBOARD STATISTICS */}
      {athletes.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2 bg-white rounded-3xl p-6 border border-slate-100 shadow-sm">
            <h3 className="font-extrabold text-slate-800 text-sm uppercase tracking-wider mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-indigo-500"></span> Distribusi Kategori
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#64748b', fontWeight: 700 }} tickLine={false} axisLine={false} />
                  <YAxis tick={{ fontSize: 10, fill: '#64748b', fontWeight: 700 }} tickLine={false} axisLine={false} />
                  <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }} />
                  <Bar dataKey="Putra" stackId="a" fill="#3b82f6" radius={[0, 0, 4, 4]} />
                  <Bar dataKey="Putri" stackId="a" fill="#ec4899" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="bg-white rounded-3xl p-6 border border-slate-100 shadow-sm flex flex-col">
            <h3 className="font-extrabold text-slate-800 text-sm uppercase tracking-wider mb-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-indigo-500"></span> Komposisi Gender
            </h3>
            <div className="flex-1 w-full flex items-center justify-center relative min-h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={genderData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                    stroke="none"
                  >
                    {genderData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-3xl font-black text-slate-800">{athletes.length}</span>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Total</span>
              </div>
            </div>
            <div className="flex justify-center gap-6 mt-4">
              {genderData.map(g => (
                <div key={g.name} className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: g.color }}></div>
                  <span className="text-xs font-bold text-slate-600">{g.name} ({g.value})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Action panel - Refresh */}"""
content = re.sub(charts_insert_point, charts_markup, content)

with open('src/components/DashboardAdmin.tsx', 'w') as f:
    f.write(content)

