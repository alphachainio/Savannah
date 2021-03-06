import operator
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q, Count, Max

from corm.models import *
from corm.connectors import ConnectionManager
from frontendv2.views import SavannahFilterView
from frontendv2.views.charts import FunnelChart

class Dashboard(SavannahFilterView):
    def __init__(self, request, community_id):
        super().__init__(request, community_id)
        self.active_tab = "dashboard"
        self._membersChart = None
        self._channelsChart = None
        self._levelsChart = None
        self.charts = set()
    
    @property 
    def member_count(self):
        members = self.community.member_set.all()
        if self.member_tag:
            members = members.filter(tags=self.member_tag)
        if self.role:
            members = members.filter(role=self.role)
        return members.count()
        
    @property 
    def conversation_count(self):
        conversations = Conversation.objects.filter(channel__source__community=self.community)
        if self.tag:
            conversations = conversations.filter(Q(tags=self.tag)|Q(speaker__tags=self.tag))
        if self.member_tag:
            conversations = conversations.filter(speaker__tags=self.member_tag)
        if self.role:
            conversations = conversations.filter(speaker__role=self.role)
        return conversations.count()
        
    @property 
    def contribution_count(self):
        contributions = Contribution.objects.filter(community=self.community)
        if self.tag:
            contributions = contributions.filter(tags=self.tag)
        if self.member_tag:
            contributions = contributions.filter(author__tags=self.member_tag)
        if self.role:
            contributions = contributions.filter(author__role=self.role)
        return contributions.count()
        
    @property 
    def contributor_count(self):
        contributors = Member.objects.filter(community=self.community)
        if self.tag:
            contributors = contributors.filter(contribution__tags=self.tag)
        if self.member_tag:
            contributors = contributors.filter(tags=self.member_tag)
        if self.role:
            contributors = contributors.filter(role=self.role)
        return contributors.annotate(contrib_count=Count('contribution')).filter(contrib_count__gt=0).count()
        
    @property
    def most_active(self):
        activity_counts = dict()
        members = Member.objects.filter(community=self.community)
        if self.role:
            members = members.filter(role=self.role)
        if self.member_tag:
            members = members.filter(tags=self.member_tag)
        if self.tag:
            members = members.annotate(conversation_count=Count('conversation', filter=Q(conversation__timestamp__gte=self.rangestart, conversation__timestamp__lte=self.rangeend, conversation__tags=self.tag)))
        else:
            members = members.filter(community=self.community).annotate(conversation_count=Count('conversation', filter=Q(conversation__timestamp__gte=self.rangestart, conversation__timestamp__lte=self.rangeend)))
        members = members.filter(conversation_count__gt=0)
        for m in members:
            activity_counts[m] = m.conversation_count
        most_active = [(member, count) for member, count in sorted(activity_counts.items(), key=operator.itemgetter(1))]
        most_active.reverse()
        return most_active[:10]

    @property
    def most_connected(self):
        members = Member.objects.filter(community=self.community)
        if self.role:
            members = members.filter(role=self.role)
        if self.member_tag:
            members = members.filter(tags=self.member_tag)
        if self.tag:
            members = members.annotate(connection_count=Count('connections', filter=Q(memberconnection__last_connected__gte=self.rangestart, memberconnection__last_connected__lte=self.rangeend, connections__tags=self.tag)))
        else:
            members = members.annotate(connection_count=Count('connections', filter=Q(memberconnection__last_connected__gte=self.rangestart, memberconnection__last_connected__lte=self.rangeend)))

        members = members.filter(connection_count__gt=0)
        connection_counts = dict()
        for m in members:
            connection_counts[m] = m.connection_count
        most_connected = [(member, count) for member, count in sorted(connection_counts.items(), key=operator.itemgetter(1))]
        most_connected.reverse()
        return most_connected[:10]

    def getMembersChart(self):
        if not self._membersChart:
            months = list()
            counts = dict()
            total = 0
            members = Member.objects.filter(community=self.community, first_seen__gte=self.rangestart, first_seen__lte=self.rangeend)
            total = Member.objects.filter(community=self.community, first_seen__lt=self.rangestart)
            if self.member_tag:
                members = members.filter(tags=self.member_tag)
                total = total.filter(tags=self.member_tag)
            if self.role:
                members = members.filter(role=self.role)
                total = total.filter(role=self.role)

            total = total.count()
            counts['prev'] = total
            members = members.order_by("first_seen")
            for m in members:
                total += 1
                month = self.trunc_date(m.first_seen)

                if month not in months:
                    months.append(month)
                counts[month] = total
            self._membersChart = (months, counts)
        return self._membersChart
        
    @property
    def members_chart_months(self):
        (months, counts) = self.getMembersChart()
        return self.timespan_chart_keys(months)

    @property
    def members_chart_counts(self):
        (months, counts) = self.getMembersChart()
        cumulative_counts = []
        previous = counts['prev']
        for month in self.timespan_chart_keys(months):
            cumulative_counts.append(counts.get(month, previous))
            previous = cumulative_counts[-1]
        return cumulative_counts
        #return [counts.get(month, 0) for month in self.timespan_chart_keys(months)]

    def getChannelsChart(self):
        channel_names = dict()
        if not self._channelsChart:
            counts = dict()
            total = 0
            conversations = Conversation.objects.filter(channel__source__community=self.community, timestamp__gte=datetime.datetime.now() - datetime.timedelta(days=self.timespan))
            if self.tag:
                conversations = conversations.filter(tags=self.tag)
            if self.member_tag:
                conversations = conversations.filter(speaker__tags=self.member_tag)
            if self.role:
                conversations = conversations.filter(speaker__role=self.role)

            conversations = conversations.annotate(source_name=F('channel__source__name'), source_connector=F('channel__source__connector')).order_by("timestamp")
            for c in conversations:
                source_name = "%s (%s)" % (c.source_name, ConnectionManager.display_name(c.source_connector))
                if source_name not in counts:
                    counts[source_name] = 1
                else:
                    counts[source_name] += 1
            self._channelsChart = [(channel, count) for channel, count in sorted(counts.items(), key=operator.itemgetter(1), reverse=True)]
            if len(self._channelsChart) > 8:
                other_count = sum([count for tag, count in self._channelsChart[7:]])
                self._channelsChart = self._channelsChart[:7]
                self._channelsChart.append(("Other", other_count, "#efefef"))
        return self._channelsChart

    @property
    def channel_names(self):
        chart = self.getChannelsChart()
        return [channel[0] for channel in chart]

    @property
    def channel_counts(self):
        chart = self.getChannelsChart()
        return [channel[1] for channel in chart]

    @property
    def levels_chart(self):
        if self._levelsChart is None:
            project = get_object_or_404(Project, community=self.community, default_project=True)
            self._levelsChart = FunnelChart(project.id, project.name, stages=MemberLevel.LEVEL_CHOICES)
            for level, name in MemberLevel.LEVEL_CHOICES:
                levels = MemberLevel.objects.filter(community=self.community, project=project, level=level)
                levels = levels.filter(timestamp__gte=self.rangestart, timestamp__lte=self.rangeend)
                if self.member_tag:
                    levels = levels.filter(member__tags=self.member_tag)
                if self.role:
                    levels = levels.filter(member__role=self.role)
                self._levelsChart.add(level, levels.count())
            self.charts.add(self._levelsChart)
        return self._levelsChart

    @login_required
    def as_view(request, community_id):
        dashboard = Dashboard(request, community_id)

        return render(request, 'savannahv2/dashboard.html', dashboard.context)
