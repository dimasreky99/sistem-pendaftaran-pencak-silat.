import re

with open('src/components/DashboardAdmin.tsx', 'r') as f:
    content = f.read()

content = content.replace('  onDeleteContingent\n}: DashboardAdminProps) {', '  onDeleteContingent,\n  onNavigateToPayment,\n  onNavigateToAthletes\n}: DashboardAdminProps) {')

with open('src/components/DashboardAdmin.tsx', 'w') as f:
    f.write(content)
