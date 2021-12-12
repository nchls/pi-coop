import React from 'react';
import { getDay, getUnixTime, fromUnixTime, parseISO } from 'date-fns';
import { 
	FlexibleWidthXYPlot, 
	XAxis, 
	YAxis, 
	HorizontalGridLines,
	VerticalGridLines, 
	LineSeries, 
	GradientDefs 
} from 'react-vis';
import { atom, useRecoilValue } from 'recoil';

import { useAPIPoll } from '../app/utils';
import './environment.scss';


const weekdays = [
	'Sun',
	'Mon',
	'Tue',
	'Wed',
	'Thu',
	'Fri',
	'Sat'
];

export const environmentState = atom({
	key: 'environment',
	default: {
		fetched: false,
		error: undefined,
		loggingEnabled: undefined,
		logEntries: {
			temperature: [],
			pressure: [],
			humidity: [],
		}
	}
});

const Environment = () => {
	useAPIPoll(environmentState, '/environment/logs', 60000 * 10);
	const environment = useRecoilValue(environmentState);

	const [earliestTimes, latestValues] = ['temperature', 'pressure', 'humidity'].reduce((accumulator, property) => {
		if (environment.logEntries[property].length === 0) {
			accumulator[0][property] = undefined;
			accumulator[1][property] = undefined;
		} else {
			accumulator[0][property] = environment.logEntries[property][0][0];
			let val = environment.logEntries[property][environment.logEntries[property].length - 1][1];
			accumulator[1][property] = Math.round(val);
		}
		return accumulator;
	}, [{}, {}]);

	const chartData = {};
	const firstInDay = {
		'temperature': [],
		'pressure': [],
		'humidity': [],
	};
	['temperature', 'pressure', 'humidity'].forEach((property) => {
		const entries = environment.logEntries[property];
		let previousDay = getDay(parseISO(earliestTimes[property]));
		chartData[property] = entries.map((entry) => {
			const dt = parseISO(entry[0]);
			const ts = getUnixTime(dt);
			if (getDay(dt) !== previousDay) {
				firstInDay[property].push(ts);
				previousDay = getDay(dt);
			}
			let val = entry[1];
			return {
				x: ts,
				y: val
			};
		});
	});

	return (
		<div className="panel is-warning environment">
			<div className="panel-heading">Coop Environment</div>
			<div className="panel-block temperature">
				<div>
					<span className="key">Temperature:</span> <span className="value">{ latestValues.temperature }°F</span>
				</div>
				<FlexibleWidthXYPlot height={150} yDomain={[-10, 120]}>
  					<HorizontalGridLines />
					<VerticalGridLines tickValues={firstInDay.temperature} />
					<LineSeries data={chartData.temperature} color="#a00" />
					<XAxis tickFormat={v => weekdays[getDay(fromUnixTime(v))]} tickValues={firstInDay.temperature} />
					<YAxis />
				</FlexibleWidthXYPlot>
			</div>
			<div className="panel-block pressure">
				<div>
					<span className="key">Pressure:</span> <span className="value">{ latestValues.pressure } mb</span>
				</div>
				<FlexibleWidthXYPlot height={150} yDomain={[970, 1040]}>
					<HorizontalGridLines />
					<VerticalGridLines tickValues={firstInDay.pressure} />
					<LineSeries data={chartData.pressure} color="#808" />
					<XAxis tickFormat={v => weekdays[getDay(fromUnixTime(v))]} tickValues={firstInDay.pressure} />
					<YAxis />
				</FlexibleWidthXYPlot>
			</div>
			<div className="panel-block humidity">
				<div>
					<span className="key">Humidity:</span> <span className="value">{ latestValues.humidity }%</span>
				</div>
				<FlexibleWidthXYPlot height={150} yDomain={[0, 100]}>
					<HorizontalGridLines />
					<VerticalGridLines tickValues={firstInDay.humidity} />
					<LineSeries data={chartData.humidity} color="#00a" />
					<XAxis tickFormat={v => weekdays[getDay(fromUnixTime(v))]} tickValues={firstInDay.humidity} />
					<YAxis />
				</FlexibleWidthXYPlot>
			</div>
		</div>
	);
};

export default Environment;
